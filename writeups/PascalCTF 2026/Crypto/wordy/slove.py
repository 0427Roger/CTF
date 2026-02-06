import socket
import sys
import numpy as np
from tqdm import tqdm
import time
from datetime import timedelta
import multiprocessing as mp

# Essayer CuPy pour GPU
try:
    import cupy as cp
    GPU_AVAILABLE = True
    print(f"[+] CuPy détecté avec GPU: {cp.cuda.runtime.getDeviceCount()} device(s)")
except:
    GPU_AVAILABLE = False
    from numba import njit, prange

ALPHABET = "abcdefghijklmnop"
K = len(ALPHABET)
L = 5
N = K ** L

def index_to_word(idx: int) -> str:
    digits = []
    x = idx
    for _ in range(L):
        digits.append(x % K)
        x //= K
    letters = [ALPHABET[d] for d in reversed(digits)]
    return "".join(letters)

def word_to_index(word: str) -> int:
    x = 0
    for ch in word:
        d = ALPHABET.find(ch)
        x = x * K + d
    return x

def wordle_feedback(guess: str, secret: str) -> str:
    res = [None] * L
    secret_counts = {}
    for i in range(L):
        s = secret[i]
        g = guess[i]
        if g == s:
            res[i] = 'G'
        else:
            secret_counts[s] = secret_counts.get(s, 0) + 1
    for i in range(L):
        if res[i] is not None:
            continue
        g = guess[i]
        if secret_counts.get(g, 0) > 0:
            res[i] = 'Y'
            secret_counts[g] -= 1
        else:
            res[i] = '_'
    return ''.join(res)

# ========== Version CPU Numba (fallback) ==========
if not GPU_AVAILABLE:
    @njit(fastmath=True, inline='always')
    def temper(y):
        y ^= (y >> 11)
        y ^= ((y << 7) & 0x9D2C5680)
        y ^= ((y << 15) & 0xEFC60000)
        y ^= (y >> 18)
        return y & 0xFFFFFFFF

    @njit(fastmath=True)
    def check_seed_cpu(seed, s0, s1, s2, s3):
        mt = np.empty(624, dtype=np.uint32)
        mt[0] = np.uint32(seed)
        for i in range(1, 624):
            mt[i] = np.uint32((1812433253 * (mt[i-1] ^ (mt[i-1] >> 30)) + i) & 0xFFFFFFFF)
        
        for i in range(624):
            y = (mt[i] & 0x80000000) | (mt[(i+1) % 624] & 0x7FFFFFFF)
            if y & 1:
                mt[i] = mt[(i+397) % 624] ^ (y >> 1) ^ 0x9908B0DF
            else:
                mt[i] = mt[(i+397) % 624] ^ (y >> 1)
        
        if (temper(mt[0]) & 0xFFFFF) != s0:
            return False
        if (temper(mt[1]) & 0xFFFFF) != s1:
            return False
        if (temper(mt[2]) & 0xFFFFF) != s2:
            return False
        if (temper(mt[3]) & 0xFFFFF) != s3:
            return False
        return True

    @njit(parallel=True, fastmath=True)
    def bruteforce_chunk_cpu(start, end, s0, s1, s2, s3):
        result = np.int64(-1)
        for seed in prange(start, end):
            if check_seed_cpu(seed, s0, s1, s2, s3):
                result = seed
        return result

# ========== Version GPU CuPy ==========
if GPU_AVAILABLE:
    mt19937_kernel = cp.RawKernel(r'''
    extern "C" __global__
    void bruteforce_mt19937(unsigned long long start_seed, 
                            unsigned int s0, unsigned int s1, 
                            unsigned int s2, unsigned int s3,
                            long long* result) {
        unsigned long long idx = blockIdx.x * blockDim.x + threadIdx.x;
        unsigned long long seed = start_seed + idx;
        
        if (seed > 0xFFFFFFFFULL) return;
        if (*result != -1) return;
        
        unsigned int mt[624];
        
        mt[0] = (unsigned int)seed;
        for (int i = 1; i < 624; i++) {
            mt[i] = (1812433253U * (mt[i-1] ^ (mt[i-1] >> 30)) + i);
        }
        
        for (int i = 0; i < 624; i++) {
            unsigned int y = (mt[i] & 0x80000000U) | (mt[(i+1) % 624] & 0x7FFFFFFFU);
            mt[i] = mt[(i+397) % 624] ^ (y >> 1) ^ ((y & 1) ? 0x9908B0DFU : 0);
        }
        
        unsigned int y;
        
        y = mt[0];
        y ^= (y >> 11);
        y ^= ((y << 7) & 0x9D2C5680U);
        y ^= ((y << 15) & 0xEFC60000U);
        y ^= (y >> 18);
        if ((y & 0xFFFFF) != s0) return;
        
        y = mt[1];
        y ^= (y >> 11);
        y ^= ((y << 7) & 0x9D2C5680U);
        y ^= ((y << 15) & 0xEFC60000U);
        y ^= (y >> 18);
        if ((y & 0xFFFFF) != s1) return;
        
        y = mt[2];
        y ^= (y >> 11);
        y ^= ((y << 7) & 0x9D2C5680U);
        y ^= ((y << 15) & 0xEFC60000U);
        y ^= (y >> 18);
        if ((y & 0xFFFFF) != s2) return;
        
        y = mt[3];
        y ^= (y >> 11);
        y ^= ((y << 7) & 0x9D2C5680U);
        y ^= ((y << 15) & 0xEFC60000U);
        y ^= (y >> 18);
        if ((y & 0xFFFFF) != s3) return;
        
        atomicCAS((unsigned long long*)result, (unsigned long long)-1, seed);
    }
    ''', 'bruteforce_mt19937')

def bruteforce_seed_optimized(secrets):
    s0, s1, s2, s3 = secrets
    total = 1 << 32
    
    if GPU_AVAILABLE:
        print(f"[+] Utilisation GPU via CuPy")
        
        threads_per_block = 256
        chunk_size = 50_000_000
        
        result = cp.array([-1], dtype=cp.int64)
        
        start_time = time.time()
        
        with tqdm(total=total, desc="GPU Bruteforce", unit="seeds", unit_scale=True) as pbar:
            for chunk_start in range(0, total, chunk_size):
                num_seeds = min(chunk_size, total - chunk_start)
                blocks = (num_seeds + threads_per_block - 1) // threads_per_block
                
                mt19937_kernel((blocks,), (threads_per_block,),
                              (chunk_start, s0, s1, s2, s3, result))
                cp.cuda.Stream.null.synchronize()
                
                res = int(result.get()[0])
                if res != -1:
                    elapsed = time.time() - start_time
                    speed = chunk_start / elapsed / 1e6
                    print(f"\n[+] Trouvé en {elapsed:.1f}s ({speed:.1f}M seeds/s)")
                    return res
                
                pbar.update(num_seeds)
        
        return None
    
    else:
        print(f"[+] Utilisation CPU parallèle ({mp.cpu_count()} cœurs)")
        print(f"[+] Compilation Numba...")
        
        bruteforce_chunk_cpu(0, 1000, s0, s1, s2, s3)
        
        num_chunks = 4096
        chunk_size = total // num_chunks
        
        start_time = time.time()
        
        with tqdm(range(num_chunks), desc="CPU Bruteforce") as pbar:
            for i in pbar:
                start = i * chunk_size
                end = start + chunk_size if i < num_chunks - 1 else total
                
                result = bruteforce_chunk_cpu(start, end, s0, s1, s2, s3)
                
                if result != -1:
                    return int(result)
                
                if i > 0:
                    elapsed = time.time() - start_time
                    speed = (i * chunk_size) / elapsed
                    eta = (total - i * chunk_size) / speed if speed > 0 else 0
                    pbar.set_postfix({"speed": f"{speed/1e6:.2f}M/s", "ETA": f"{int(eta)}s"})
        
        return None

class MT19937:
    def __init__(self, seed):
        self.mt = [0] * 624
        self.index = 624
        self.mt[0] = seed & 0xFFFFFFFF
        for i in range(1, 624):
            self.mt[i] = (1812433253 * (self.mt[i-1] ^ (self.mt[i-1] >> 30)) + i) & 0xFFFFFFFF
    
    def twist(self):
        for i in range(624):
            y = (self.mt[i] & 0x80000000) | (self.mt[(i+1) % 624] & 0x7FFFFFFF)
            self.mt[i] = self.mt[(i+397) % 624] ^ (y >> 1) ^ (0x9908B0DF if (y & 1) else 0)
        self.index = 0
    
    def next_u32(self):
        if self.index >= 624:
            self.twist()
        y = self.mt[self.index]
        self.index += 1
        y ^= (y >> 11)
        y ^= ((y << 7) & 0x9D2C5680)
        y ^= ((y << 15) & 0xEFC60000)
        y ^= (y >> 18)
        return y & 0xFFFFFFFF

# ========== Communication robuste ==========
def recv_line(sock):
    data = b""
    while not data.endswith(b"\n"):
        chunk = sock.recv(1)
        if not chunk:
            break
        data += chunk
    return data.decode().strip()

def recv_until(sock, marker, timeout=5):
    """Reçoit jusqu'à trouver un marqueur"""
    sock.settimeout(timeout)
    data = ""
    try:
        while marker not in data:
            chunk = sock.recv(1024).decode()
            if not chunk:
                break
            data += chunk
    except socket.timeout:
        pass
    sock.settimeout(None)
    return data

def solve_secret(sock, all_words):
    possible = set(all_words)
    attempts = 0
    max_attempts = 20  # Sécurité
    
    while len(possible) > 1 and attempts < max_attempts:
        attempts += 1
        guess = next(iter(possible))
        sock.send(f"GUESS {guess}\n".encode())
        response = recv_line(sock)
        
        print(f"    Guess: {guess} -> {response}")
        
        if "FEEDBACK" not in response.upper():
            # Peut-être CORRECT ou autre chose
            if "CORRECT" in response.upper() or "WIN" in response.upper():
                return word_to_index(guess)
            print(f"[!] Réponse inattendue: {response}")
            continue
        
        # Extraire le feedback (format: "FEEDBACK GGYY_" ou similaire)
        parts = response.split()
        if len(parts) >= 2:
            feedback = parts[1]
        else:
            feedback = response.replace("FEEDBACK", "").strip()
        
        possible = {w for w in possible if wordle_feedback(guess, w) == feedback}
        print(f"    Remaining: {len(possible)}")
        
        if len(possible) == 0:
            print("[!] Plus de mots possibles!")
            return None
    
    if len(possible) == 1:
        final_word = possible.pop()
        # Soumettre le mot final
        sock.send(f"GUESS {final_word}\n".encode())
        response = recv_line(sock)
        print(f"    Final: {final_word} -> {response}")
        return word_to_index(final_word)
    
    return None

def main():
    HOST = "wordy.ctf.pascalctf.it"
    PORT = 5005
    
    print("[+] Génération des mots...")
    all_words = [index_to_word(i) for i in range(N)]
    
    print(f"[+] Connexion à {HOST}:{PORT}...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    
    # Lire le banner
    print("[+] Attente du banner...")
    banner = recv_until(sock, "READY", timeout=10)
    print("=" * 50)
    print(banner)
    print("=" * 50)
    
    if "READY" not in banner:
        print("[!] READY non reçu, tentative de continuer...")
    
    secrets = []
    for rnd in range(1, 5):
        print(f"\n{'='*20} Round {rnd}/4 {'='*20}")
        sock.send(b"NEW\n")
        
        response = recv_line(sock)
        print(f"[+] Réponse NEW: {response}")
        
        idx = solve_secret(sock, all_words)
        if idx is None:
            print("[!] Échec résolution du secret")
            return
        secrets.append(idx)
        print(f"[+] Secret trouvé: {index_to_word(idx)} (idx={idx})")
    
    print(f"\n[+] Secrets collectés: {secrets}")
    print(f"[+] En mots: {[index_to_word(s) for s in secrets]}")
    
    print("\n[*] Lancement du bruteforce...")
    seed = bruteforce_seed_optimized(secrets)
    
    if seed is None:
        print("[!] Graine non trouvée")
        return
    
    print(f"\n[+] GRAINE TROUVÉE: {seed}")
    
    # Vérification
    rng = MT19937(seed)
    print("[+] Vérification:")
    for i, expected in enumerate(secrets):
        got = rng.next_u32() & 0xFFFFF
        status = "✓" if got == expected else "✗"
        print(f"    {i+1}: attendu={expected}, obtenu={got} {status}")
    
    print("\n[+] Soumission des prédictions:")
    for i in range(5):
        idx = rng.next_u32() & 0xFFFFF
        word = index_to_word(idx)
        sock.send(f"FINAL {word}\n".encode())
        resp = recv_line(sock)
        print(f"  {i+1}/5: {word} -> {resp}")
    
    # Récupérer tout ce qui reste
    print("\n[+] Réponse finale:")
    try:
        final = recv_until(sock, "}", timeout=5)
        print(final)
    except:
        pass
    
    sock.close()

if __name__ == "__main__":
    main()

from pwn import *
import re

#context.log_level = 'debug'
io = remote("penguin.ctf.pascalctf.it", 5003)

words = [
    "biocompatibility", "biodegradability", "characterization", "contraindication",
    "counterbalancing", "counterintuitive", "decentralization", "disproportionate",
    "electrochemistry", "electromagnetism", "environmentalist", "internationality",
    "internationalism", "institutionalize", "microlithography", "microphotography",
    "misappropriation", "mischaracterized", "miscommunication", "misunderstanding",
    "photolithography", "phonocardiograph", "psychophysiology", "rationalizations",
    "representational", "responsibilities", "transcontinental", "unconstitutional"
]

idx=0
enc_map={}
for _ in range(7):
    for _ in range(4):
        io.recvuntil(b"Word")
        io.recvuntil(b":")
        io.sendline(words[idx].encode())
        idx+=1
    io.recvuntil(b"Encrypted words: ")
    line = io.recvline()
    blocks=re.findall(br'[0-9a-zA-Z]{32}',line)

    for c,w in zip(blocks,words[idx-4:idx]):
        enc_map[c.decode()]=w

io.recvuntil(b"Ciphertext: ")
ct_line=io.recvline().strip()
ct_block=ct_line.decode().split()
for i,c in enumerate(ct_block):
    guess=enc_map[c]
    io.sendlineafter(f"Guess the word {i+1}: ".encode(),guess.encode())
io.interactive()
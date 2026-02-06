# **XorD**

> This write-up documents a deliberately vulnerable lab / CTF-style service.  
> All techniques are presented for educational purposes only.

------

## Overview

- **Category**: Cryptography
- **Difficulty**: Easy
- **Key Concept**: Pseudo-Random Number Generator (PRNG), XOR Operation
- **Goal**: ` Recover the flag using the property (A ^ B) ^ B = A`

------

## Challenge Description

​	I just discovered bitwise operators, so I guess 1 XOR 1 = 1?

```python
#xord.py
import os
import random

def xor(a, b):
    return bytes([a ^ b])

flag = os.getenv('FLAG', 'pascalCTF{REDACTED}')
encripted_flag = b''
random.seed(1337)

for i in range(len(flag)):
    random_key = random.randint(0, 255)
    encripted_flag += xor(ord(flag[i]), random_key)

with open('output.txt', 'w') as f:
    f.write(encripted_flag.hex())
```

**Output:**
`cb35d9a7d9f18b3cfc4ce8b852edfaa2e83dcd4fb44a35909ff3395a2656e1756f3b505bf53b949335ceec1b70e0`

## Key Concepts

### 1. `random.seed()`

**Full Name**: Initialize internal state of the random number generator.
**Function**: Determines the starting point for the PRNG. If the seed is fixed, the sequence of numbers generated will always be identical.
**Example**:

```python
random.seed(42)
print(random.random()) # Always returns 0.6394...
```

### 2. XOR Operation (`^`)

**Full Name**: Exclusive OR.
**Function**: A bitwise operator where the output is true only if the inputs differ. It is reversible.
**Example**:

```python
# XOR Truth Table: 0^0=0, 0^1=1, 1^0=1, 1^1=0

# Encrypt: 
# A (Plain): 0101 (5)
# B (Key)  : 0011 (3)
# 5 ^ 3 = 6 
# Result   : 0110 (6)

# Decrypt:
# Result   : 0110 (6)
# B (Key)  : 0011 (3)
# 6 ^ 3 = 5
# A (Plain): 0101 (5)
```

------

## Solution

**Observation**:
The script uses `random.seed(1337)`. This is a hardcoded seed. This means we can reproduce the exact same sequence of `random_key` values on our local machine.

**Logic**:
`Ciphertext[i] ^ Key[i] = Flag[i]`

**Solver Script**:

```python
import random

# 1. Set the same seed to reproduce the key stream
random.seed(1337)

# 2. Load the ciphertext
output_hex = "cb35d9a7d9f18b3cfc4ce8b852edfaa2e83dcd4fb44a35909ff3395a2656e1756f3b505bf53b949335ceec1b70e0"
ciphertext = bytes.fromhex(output_hex)

flag = ''

# 3. Decrypt byte by byte
for byte in ciphertext:
    # Important: Generate the key inside the loop to match the encryption order
    key = random.randint(0, 255) 
    flag += chr(byte ^ key)

print(flag) #pascalCTF{1ts_4lw4ys_4b0ut_x0r1ng_4nd_s33d1ng}
```

## Key Takeaways

- **PRNG Vulnerability**: The standard `random` module in Python is predictable. Never use it for cryptography.
- **Hardcoded Seeds**: If an attacker knows the seed, they know the entire random sequence. Use `secrets` module or hardware entropy for secure keys.


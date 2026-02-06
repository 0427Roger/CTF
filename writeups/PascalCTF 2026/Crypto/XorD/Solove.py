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
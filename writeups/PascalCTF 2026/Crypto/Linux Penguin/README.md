# **Linux Penguin**

> This write-up documents a deliberately vulnerable lab / CTF-style service.  
> All techniques are presented for educational purposes only.

------

## Overview

- **Category**: Cryptography
- **Difficulty**: Easy
- **Key Concept**: Deterministic encryption mapping
- **Goal**: Identify encrypted words and retrieve the flag

------

## Challenge Description

​	I've just installed Arch Linux and I couldn't be any happier :)

During the interaction:

- The server asks for words and returns their encrypted values
- At the end, a ciphertext containing several encrypted words is shown
- Correctly identifying all encrypted words reveals the flag

## Solution Approach

​	The challenge can be solved by **recording encryption outputs and reusing them**.

### Step 1: Collect Encryption Results

The server allows the user to submit words and immediately returns their encrypted form.

By submitting all available words:

- Each word’s encrypted value is recorded

- A simple mapping is created:

  `encrypted_value → original_word`

  ### Step 2: Match the Final Ciphertext

  When the final encrypted message is displayed:

  - The ciphertext is split into individual encrypted values
  - Each value is matched against the previously recorded mapping
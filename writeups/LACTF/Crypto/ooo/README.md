# **ooo**

> This write-up documents a deliberately vulnerable lab / CTF-style service.  
> All techniques are presented for educational purposes only.

---

## Overview

- **Category**: Reversing / Python
- **Difficulty**: Easy
- **Key Concepts**: Unicode homoglyphs, operator mapping, algebraic simplification, chain encoding
- **Goal**: Recover the flag from an obfuscated verifier

---

## Challenge Description

> Surely everyone knows the difference between the Cyrillic small letter o, the Greek small letter omicron, and the Latin small letter o, right? :)

---

## Analysis

### Initial Observation
The challenge provides a Python flag checker that defines many functions whose names look almost identical (e.g., `о`, `ο`, `օ`, `ỏ`, `ơ`, …).
 These identifiers are **Unicode homoglyphs** (different code points that render similarly), used to make the logic hard to read.

The script checks an input `guess` against a list of integers `ὁ` (the “encoder” array). It iterates over adjacent characters in the guess, computes two `ord()` values, and compares a derived expression to an indexed element of `ὁ`.

---

### Root Cause / Weakness
The obfuscation relies on:

1. **Homoglyph confusion**: visually similar function names hide simple operations.
2. **Dead / misleading math**: an index expression contains `(a*b) % a`, which always becomes `0` (when `a != 0`), collapsing the “complex” index into a simple one.
3. **Linear relation**: the verifier ultimately enforces a basic equation on adjacent characters, making the flag recoverable via a straightforward recurrence once one character is known.

---

## Key Concepts

### Unicode Homoglyphs

Unicode allows letters from different scripts (Latin, Greek, Cyrillic, Armenian, etc.) that look very similar on screen.
 In Python, these are **distinct identifiers**, so you can define multiple functions that *appear* to be named “o” but are actually different characters.

This is commonly used in CTF reversing to defeat quick visual inspection and copy/paste reasoning.

### Algebraic Simplification in Verifiers

Many “complex” verifiers hide a simple invariant. Here, the critical simplification is:

- `(x * y) % x == 0` for `x != 0`
- `i ^ 0 == i` (XOR with zero)

These collapse the indexing expression so the comparison becomes a direct constraint on the current and next character.

---

## Exploitation / Solution

### Step 1 – !Step_Title
### Step 1 – Deobfuscate Operations and Simplify the Condition

From the provided code:

- `о(a,b)` returns `a + b`
- `ơ(a,b)` returns `a ^ b`
- `ȯ(a,b)` returns `a % b`
- `ὄ(a,b)` returns `a`
- `ὂ(a,b)` returns `b`

Let:

- `x = ord(guess[i])`
- `y = ord(guess[i+1])`

The verifier checks:

- Left side: `о(ὄ( x,y ), ὂ( x,y )) = x + y`
- Index: `ơ(i, ȯ(օ(x,y), x))`
  - `օ(x,y) = x*y`
  - `ȯ(x*y, x) = (x*y) % x = 0`
  - `ơ(i, 0) = i`

So the condition reduces to:

```
ord(guess[i]) + ord(guess[i+1]) == ὁ[i]
```

That means `ὁ` is a chain encoding of adjacent character sums.

### Step 2 – Reconstruct the Flag via Recurrence

Rearrange:

```
guess[i+1] = ὁ[i] - guess[i]
```

Once you know the first character, you can recover the entire string deterministically.
 Since flags start with `lactf{`, knowing the first character `"l"` is sufficient.

```python
flagencoder=[205, 196, 215, 218, 225, 226, 1189, 2045, 2372, 9300, 8304, 660, 8243, 16057, 16113, 16057, 16004, 16007, 16006, 8561, 805, 346, 195, 201, 154, 146, 223]
flag = "l" # remember, flags start with lactf{

for i in range(len(flagencoder)):
    next_char = chr(flagencoder[i] - ord(flag[i]))
    flag += next_char

print(flag)
```

Recovered flag:

```
lactf{wow_so_unicode_very_arabic}
```

------

## Key Takeaways

- Unicode homoglyphs can make code look familiar while being entirely different identifiers; always copy names carefully or normalize them during analysis.
- Look for algebraic identities that collapse “scary” expressions (e.g., `(a*b) % a = 0`, `x ^ 0 = x`)—CTF obfuscation often depends on you missing these.
- Chain encodings (adjacent sums / differences / XORs) are reversible with a simple recurrence once you know one starting character.

------

## References

- Python documentation: Unicode identifiers (valid identifier characters and normalization rules)
- Unicode Security: confusables / homoglyphs (why visually similar characters are risky)
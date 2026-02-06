# **AuraTester2000**

> This write-up documents a deliberately vulnerable lab / CTF-style service.  
> All techniques are presented for educational purposes only.

------

## Overview

- **Category**: Misc / Reversing
- **Difficulty**: Easy
- **Key Concept**: Source code analysis, custom encoding logic
- **Goal**: Recover the original phrase from a custom encoder to obtain the flag

------

## Challenge Description

​	Will you be able to gain enogh aura?

## 1. Analysis

​	The provided source code appears intentionally obfuscated using meme-style syntax, replacing standard Python keywords with slang expressions. After translating these expressions back into valid Python syntax, the program structure becomes clear.

The application generates two important random values at runtime:

```
phrase = random selection of 3–5 words from a predefined list
steps = random integer between 2 and 5
```

## 2. Encoder Logic

The encoder function applies a position-based transformation to the phrase.

### Encoding Rules

For each character in the phrase:

1. If the character is a space → keep it unchanged
2. If the index of the character is divisible by `steps` → convert the character to its ASCII value
3. Otherwise → keep the character unchanged

Simplified encoder logic:

```python
for i in range(len(phrase)):
    if phrase[i] == " ":
        output += " "
    elif i % steps == 0:
        output += str(ord(phrase[i]))
    else:
        output += phrase[i]
```

### Example

If:

```
phrase = "hello world"
steps = 2
```

Encoded result:

```
104e108l111 119o114l100
```

This encoding is reversible because ASCII numbers can be converted back into characters.

## 3. Program Flow

​	The application contains an aura scoring system which initially appears necessary to unlock the final test. However, analysis shows that aura is only used as a gate condition:

```python
if aura < 500:
    deny access
else:
    allow final test
```

​	The aura score can be manipulated easily by answering the provided questions, making it irrelevant to the core challenge.![1770285171147](image/image1.png)

​	The source code provides scoring rules, so if we answer `yes, no, yes, no`, the score will reach the target of 500.

## 4.Solution

​	When you score reaches the target, we can proceed to the next stage.

It say:

```
If you want to win your prize you need to decode this secret phrase:
102ilip112o bo115chi 108akak97 tra108lale114o tu110gtun103 cuc105nato
```

​	The source code provides words.

```python
words = [
    "tungtung",
    "trallalero",
    "filippo boschi",
    "zaza",
    "lakaka",
    "gubbio",
    "cucinato"
]
```

Therefore, we can match words:

```
filippo boschi lakaka trallalero tungtung cucinato
```

## Key Takeaways

- Custom encoding functions are often reversible when deterministic rules are used.

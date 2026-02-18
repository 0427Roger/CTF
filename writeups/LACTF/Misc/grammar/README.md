# **grammar**

> This write-up documents a deliberately vulnerable lab / CTF-style service.  
> All techniques are presented for educational purposes only.

---

## Overview

- **Category**: Misc
- **Difficulty**: Easy
- **Key Concepts**: Context-Free Grammar (CFG), EBNF, Parse Tree Reconstruction
- **Goal**: Recover the full flag.

---

## Challenge Description

> ​	Inspired by CS 131 Programming Languages, I decided to make a context-free grammar in EBNF for my flag! But it looks like some squirrels have eaten away at the parse tree...

The challenge provides a visual representation of a parse tree.
![Parse Tree](src/tree.png)

---

## Analysis

### Initial Observation
The `grammar-notes.txt` file defines the rules for the flag's structure in EBNF, which is crucial for this challenge.
```ebnf  
flag = start, word, {underscore, word}, end;  
start = "l", "a", "c", "t", "f", "{";  
end = "}";  
underscore = "_";  
word = fragment, {fragment};  
fragment = cd | vc | vd | c | d;  
cd = con, dig;  
vc = vow, con;  
vd = vow, dig;  
c = con;  
d = dig;  
con = "f" | con2;  
con2 = "g" | con3;  
con3 = "p" | con4;  
con4 = "t" | con5;  
con5 = "r";  
vow = "e" | vow2;  
vow2 = "o" | vow3;  
vow3 = "u";  
dig = "0" | dig2;  
dig2 = "1" | dig3;  
dig3 = "4" | dig4;  
dig4 = "5";  
```

From this grammar, we can derive the character sets for `con` (consonants), `vow` (vowels), and `dig` (digits):

- `con` = {"f", "g", "p", "t", "r"}
- `vow` = {"e", "o", "u"}
- `dig` = {"0", "1", "4", "5"}

The image displays a tree where the bottom-most black circles are stacked. The number of circles in a stack (let's call it `stack_height`) directly corresponds to an index within the respective character set (e.g., `stack_height - 1`). For example, a stack of 1 circle would correspond to index 0, a stack of 2 circles to index 1, and so on.

The image structure shows:

- `flag = start, word1, underscore, word2, underscore, word3, end`
- Each `word` is composed of `fragment`s.
- Each `fragment` corresponds to a colored circle in the tree, with a specific type (`cd`, `vc`, `vd`, `c`, or `d`) and its associated stack(s) of black circles.

---

### Root Cause / Weakness
The core “weakness” is that the tree’s labels (nonterminal names like `cd`, `vc`, `vd`) are partially missing, but the remaining visual structure leaks enough information to reconstruct them.

Two design choices make recovery possible:

1. **Arity leak (1-stack vs 2-stack)**
    Even without text labels, the tree shape reveals whether a fragment expands into one terminal (`c`/`d`) or two terminals (`cd`/`vc`/`vd`).
2. **Alphabet-size constraints**
    The sets have different sizes (`|con|=5`, `|dig|=4`, `|vow|=3`).
    The maximum possible stack height under each subtree uniquely indicates whether that stack must represent `con`, `dig`, or `vow` (e.g., a height of 5 can only be `con`).

As a result, each fragment’s type and its characters can be recovered purely from **stack heights + grammar constraints**, even though parts of the parse tree are “eaten”.

---

## Key Concepts

### Context-Free Grammar (CFG)

A CFG describes how a language can be generated using production rules.
 Each rule rewrites a **nonterminal** into terminals and/or other nonterminals.
 This challenge uses CFG rules to constrain the exact structure of the flag and the allowed characters.

### Extended Backus–Naur Form (EBNF)

EBNF is a notation for writing CFGs with convenience operators such as:

- `{ ... }` meaning repetition (0 or more)
- `|` meaning alternatives
- quoted strings meaning literal terminals

Here, the grammar explicitly defines both:

- the overall flag format (`lactf{...}`)
- the internal word structure (built from `fragment`s)

### Parse Tree Reconstruction

A parse tree is a concrete derivation showing how the start symbol expands into terminals.
 Even when labels are missing, if the tree still encodes:

- branching structure
- arity (how many children)
- positional information
   then it can still be reverse-engineered.

---

## Exploitation / Solution

### Step 1 – Identify the high-level layout

From the top level of the tree, we read:

- `start` produces `lactf{`
- then we have `word1`, `_`, `word2`, `_`, `word3`
- `end` produces `}`

So the flag format is:

```
lactf{word1_word2_word3}
```

### Step 2 – Decode each fragment using stack heights

For each colored fragment node:

1. Count how many stacks it has:
   - 1 stack → `c` or `d`
   - 2 stacks → one of `cd`, `vc`, `vd`
2. For each stack:
   - compute `index = height - 1`
   - map index into `con`, `vow`, or `dig`
3. Use grammar constraints to decide which set applies:
   - if a stack height exceeds 3, it cannot be `vow`
   - if a stack height reaches 5, it must be `con`
4. Concatenate characters in left-to-right order within the fragment.
5. Concatenate fragments in left-to-right order within each word.

### Step 3 – Reconstruct the full flag

After decoding all fragments under the three `word` nodes and inserting underscores, the recovered flag is:

```
lacft{pr0fe55or_p4u1_eggert}
lactf{4r00e5tor_p4u1_eg1er5}
```

---

## Key Takeaways

- A CFG/EBNF can fully define a structured string format, including nested constraints.
- Even when labels are removed, a parse tree can leak information through structure (arity) and bounded alphabets.
- “Visual encodings” (like stack heights) are effectively just another representation of indices; once recognized, reconstruction becomes mechanical.

------

## References

- Wikipedia: Context-free grammar (CFG)
- Wikipedia: Extended Backus–Naur form (EBNF)
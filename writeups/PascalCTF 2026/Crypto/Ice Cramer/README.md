# **Ice Cramer**

> This write-up documents a deliberately vulnerable lab / CTF-style service.  
> All techniques are presented for educational purposes only.

------

## Overview

- **Category**: Algebra / Matrix Operations
- **Difficulty**: Easy
- **Key Concept**: Extract numerical coefficients using regex , solve a linear system
- **Goal**: Recover the flag by solving a system of linear equations

------

## Challenge Description

​	Elia’s swamped with algebra but craving a new ice-cream flavor, help him crack these equations so he can trade books for a cone!

```python
#main.py
import os
from random import randint

def generate_variable():
    flag = os.getenv("FLAG", "pascalCTF{REDACTED}") # The default value is a placeholder NOT the actual flag
    flag = flag.replace("pascalCTF{", "").replace("}", "")
    x = [ord(i) for i in flag]
    return x

def generate_system(values):
    for _ in values:
        eq = []
        sol = 0
        for i in range(len(values)):
            k = randint(-100, 100)
            eq.append(f"{k}*x_{i}")
            sol += k * values[i]

        streq = " + ".join(eq) + " = " + str(sol)
        print(streq)


def main():
    x = generate_variable()
    generate_system(x)
    print("\nSolve the system of equations to find the flag!")

if __name__ == "__main__":
    main()
```

```
#output.txt
26*x_0 + -97*x_1 + -18*x_2 + 99*x_3 + ... + 35*x_27 = 2325
-59*x_0 + -45*x_1 + -23*x_2 + 51*x_3 + ... + -18*x_27 = -28918
...
(28 equations total)
```

## 1. Analysis

The program converts the flag into a list of ASCII values and generates a **28×28 linear system**:
$$
A \cdot x = b
$$
Where:

- **A** is the coefficient matrix
- **x** is the vector of unknown ASCII values
- **b** is the result vector

### Extracting Data with Regex

We use `regex` to extract:

- The coefficients of each variable
- The values on the right-hand side of each equation

```python
import re

s=open('./source/output.txt').read()
pat = re.findall(r"([-]?\d+)\*x_\d+",s)
solu=re.findall(r'= ([-]?\d+)',s)
```

### Grouping the Coefficients

​	Each equation contains 28 coefficients. We group them accordingly to form the matrix.

```python
patt=[]
lists=[]
for i in pat:
    patt.append(i)
    if len(patt)>=28:
        lists.append(patt)
        patt=[]
```

### Solving the Matrix

We use `sympy.Matrix` to solve the linear system.

```python
from sympy import Matrix

A = Matrix(lists)                 # Coefficient matrix
b = Matrix([int(i) for i in solu])

x = A.LUsolve(b)
```

### Recovering the Flag

The solution vector contains ASCII values, which can be converted back into characters.

```python
flag=''.join([chr(i) for i in x]) 
print(flag)			#0h_My_G0DD0_too_much_m4th_:O
```

---

## Key Takeaways

- This challenge is purely **linear algebra**, not exploitation
- Regex is useful for extracting structured numerical data
- A system of equations can be directly mapped to a matrix form
- Converting between ASCII values and characters is a common CTF pattern



## References

- SymPy Matrix Documentation
- Linear Algebra: Solving  *A*\*x*=*b
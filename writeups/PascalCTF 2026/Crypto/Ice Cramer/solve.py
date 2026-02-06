import re
from sympy import Matrix

s = open('./source/output.txt').read()

pat  = re.findall(r"([-]?\d+)\*x_\d+", s)
solu = re.findall(r"= ([-]?\d+)", s)

rows = []
row = []

for i in pat:
    row.append(int(i))
    if len(row) == 28:
        rows.append(row)
        row = []

A = Matrix(rows)
b = Matrix([int(i) for i in solu])

x = A.LUsolve(b)

print(''.join(chr(int(i)) for i in x))
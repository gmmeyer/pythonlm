# ladder with 1, 2 or 3 rungs per move: ways to reach rung 10
a = 1
b = 1
c = 2
for rung in range(3, 11):
    nxt = a + b + c
    a = b
    b = c
    c = nxt
print(c)

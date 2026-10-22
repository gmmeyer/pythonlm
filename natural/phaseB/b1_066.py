# triangular numbers that are also perfect squares
t = 0
for i in range(1, 9):
    t += i
    r = 0
    while r * r < t:
        r += 1
    if r * r == t:
        print(t)

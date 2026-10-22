s = "ab"
steps = 0
while len(s) + len(s) <= 48:
    s = s + s
    steps += 1
print(steps, len(s))
print(s)
print(s[-1], s[-2], s[-len(s)], s[len(s) // 2])

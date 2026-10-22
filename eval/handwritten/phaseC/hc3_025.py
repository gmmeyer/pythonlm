s = "Stressed!"
r = ""
i = len(s) - 1
while i >= 0:
    r += s[i]
    i -= 1
print(r)
r2 = ""
for k in range(1, len(s) + 1):
    r2 = r2 + s[-k]
print(r2, r == r2, len(r2))

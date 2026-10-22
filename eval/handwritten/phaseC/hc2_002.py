s = "mississippi"
c = "s"
n = 0
last = -1
for i in range(len(s)):
    if s[i] == c:
        n += 1
        last = i
print(c, n, last, sep=":")

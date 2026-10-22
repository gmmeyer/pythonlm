s = "pythonic"
n = len(s)
print(s[-1], s[-n], s[n - 1], s[0])
i = -1
out = ""
while i >= -n:
    out = out + s[i]
    i -= 1
print(out, len(out))
print(s[-n] == s[0], s[-1] != s[n - 1])
print(f"{s[-2]}{s[-3]}{s[1 - n]}")

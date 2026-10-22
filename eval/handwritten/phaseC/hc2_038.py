a = "interval"
b = "internet"
c = "interior"
p = ""
i = 0
while i < len(a) and i < len(b) and i < len(c):
    if a[i] != b[i] or a[i] != c[i]:
        break
    p += a[i]
    i += 1
print("prefix:", p, "len", len(p))

a = "ACE"
b = "bdfgh"
out = ""
i = 0
while i < len(a) or i < len(b):
    if i < len(a):
        out += a[i]
    if i < len(b):
        out += b[i]
    i += 1
print(out, len(out))

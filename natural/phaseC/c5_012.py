a = "interstellar"
b = "internal"
n = len(a)
if len(b) < n:
    n = len(b)
pos = 0
while pos < n and a[pos] == b[pos]:
    pos += 1
print("common prefix length:", pos)

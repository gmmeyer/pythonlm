x = "running"
y = "jumping"
k = 0
suf = ""
while k < len(x) and k < len(y) and x[-1 - k] == y[-1 - k]:
    suf = x[-1 - k] + suf
    k += 1
print(f"common suffix '{suf}' of length {k}")

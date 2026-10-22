packed = "a3b2c4"
out = ""
for i in range(0, len(packed), 2):
    ch = packed[i]
    n = 0
    for k in range(10):
        if str(k) == packed[i + 1]:
            n = k
    out += ch * n
print(packed, "->", out)

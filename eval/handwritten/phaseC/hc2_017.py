code = "a3b1c4d2"
out = ""
i = 0
while i < len(code):
    ch = code[i]
    d = 0
    while str(d) != code[i + 1]:
        d += 1
    out += ch * d
    i += 2
print(code, "=>", out)

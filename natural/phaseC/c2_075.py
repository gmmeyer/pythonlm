code = "1011201"
valid = True
bad = -1
for i in range(len(code)):
    if code[i] != "0" and code[i] != "1":
        if valid:
            bad = i
        valid = False
if valid:
    print(code, "is a binary string")
else:
    print(code, "is not binary; first bad digit at", bad)

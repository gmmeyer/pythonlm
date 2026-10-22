out = ""
for n in range(1, 8):
    out += str(n * n)
    if n < 7:
        out += ","
print(out)
print("length", len(out))

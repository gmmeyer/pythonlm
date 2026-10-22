bits = "101101"
value = 0
for i in range(len(bits)):
    value = value * 2
    if bits[i] == "1":
        value += 1
print(bits, "=", value)

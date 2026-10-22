code = "a7b3c9"
total = 0
for i in range(len(code)):
    c = code[i]
    if "0" <= c <= "9":
        for k in range(10):
            if str(k) == c:
                total += k
print("sum of digits:", total)

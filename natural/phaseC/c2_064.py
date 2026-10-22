a = "1011"
b = "0110"
carry = 0
result = ""
for i in range(len(a) - 1, -1, -1):
    total = carry
    if a[i] == "1":
        total += 1
    if b[i] == "1":
        total += 1
    result = str(total % 2) + result
    carry = total // 2
if carry == 1:
    result = "1" + result
print(a, "+", b, "=", result)

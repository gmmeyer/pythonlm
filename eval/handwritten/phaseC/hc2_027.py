a = "110101"
b = "1011"
i = len(a) - 1
j = len(b) - 1
carry = 0
s = ""
while i >= 0 or j >= 0 or carry > 0:
    t = carry
    if i >= 0 and a[i] == "1":
        t += 1
    if j >= 0 and b[j] == "1":
        t += 1
    s = str(t % 2) + s
    carry = t // 2
    i -= 1
    j -= 1
print(a, "+", b, "=", s)

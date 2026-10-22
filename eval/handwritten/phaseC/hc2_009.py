abc = "abcdefghijklmnopqrstuvwxyz"
w = "fade"
total = 0
for i in range(len(w)):
    p = 0
    while abc[p] != w[i]:
        p += 1
    total += (i + 1) * (p + 1)
chk = abc[total % 26]
print(w + "-" + chk, total)

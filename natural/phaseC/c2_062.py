a = "listen"
b = "silent"
same = len(a) == len(b)
for i in range(len(a)):
    ca = 0
    cb = 0
    for j in range(len(a)):
        if a[j] == a[i]:
            ca += 1
    for j in range(len(b)):
        if b[j] == a[i]:
            cb += 1
    if ca != cb:
        same = False
print(a, b, "anagrams?", same)

a = "stop"
b = "post"
same = len(a) == len(b)
i = 0
while same and i < len(a):
    ca = 0
    cb = 0
    for j in range(len(a)):
        if a[j] == a[i]:
            ca += 1
        if b[j] == a[i]:
            cb += 1
    if ca != cb:
        same = False
    i += 1
print(a, b, same)

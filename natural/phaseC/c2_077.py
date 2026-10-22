a = "abcde"
b = "cdeab"
n = len(a)
found = -1
for k in range(n):
    match = True
    for i in range(n):
        if a[(i + k) % n] != b[i]:
            match = False
            break
    if match:
        found = k
if found == -1:
    print(b, "is not a rotation of", a)
else:
    print(b, "is", a, "rotated by", found)

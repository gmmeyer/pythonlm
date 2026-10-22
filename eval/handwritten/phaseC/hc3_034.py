a = "1001011001"
b = "1001001001"
i = 0
while i < len(a) and a[i] == b[i]:
    i += 1
print("differ at", i, a[i], b[i])
diffs = 0
for j in range(len(a)):
    if a[j] != b[j]:
        diffs += 1
print(diffs, a == b, a != b)
c = "1001" + "011001"
print(c == a, c)

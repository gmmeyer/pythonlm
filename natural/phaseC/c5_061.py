a = "planet"
b = "plane"
i = 0
while i < len(a) and i < len(b) and a[i] == b[i]:
    i += 1
if i == len(a) and i == len(b):
    print("equal")
elif i == len(b):
    print(b, "is a prefix, so it comes first")
elif i == len(a):
    print(a, "is a prefix, so it comes first")
elif a[i] < b[i]:
    print(a, "comes first because", a[i], "<", b[i])
else:
    print(b, "comes first because", b[i], "<", a[i])

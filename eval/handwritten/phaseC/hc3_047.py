target = "aaab"
s = "b"
while s != target:
    s = "a" + s
    print(s, len(s), s == target)
print("done", s)

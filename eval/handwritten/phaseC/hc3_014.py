s = "xyxyyx"
n = len(s)
same = 0
diff = 0
for i in range(n // 2):
    left = s[i]
    right = s[-1 - i]
    print(i, left, right, left == right)
    if left == right:
        same += 1
    else:
        diff += 1
print(f"same={same} diff={diff}")
r = ""
for i in range(n):
    r = s[i] + r
print(r, r == s, r != "xyyxyx")

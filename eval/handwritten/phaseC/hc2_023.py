p = "(()(()))()(("
depth = 0
deep = 0
ok = True
for i in range(len(p)):
    if p[i] == "(":
        depth += 1
        if depth > deep:
            deep = depth
    else:
        depth -= 1
        if depth < 0:
            ok = False
            break
if depth != 0:
    ok = False
print("balanced:", ok, "max depth:", deep, "open:", depth)

expr = "(a+(b*c))-(d"
depth = 0
ok = True
for i in range(len(expr)):
    if expr[i] == "(":
        depth += 1
    elif expr[i] == ")":
        depth -= 1
        if depth < 0:
            ok = False
if depth != 0:
    ok = False
print(expr, "balanced?", ok)

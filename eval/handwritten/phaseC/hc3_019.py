a = "0"
b = " "
c = ""
print(not a, not b, not c)
print("[" + (a or "x") + "]", "[" + (b or "x") + "]", "[" + (c or "x") + "]")
print("[" + (a and "y") + "]", "[" + (c and "y") + "]")
if b:
    print("space is truthy", len(b))
if not c:
    print("empty is falsy", len(c))
print(not not a, not not c)

# Letter histogram of a phrase, read one character at a time.
s = "banana bandana cab"
na = nb = nn = other = 0
i = 0
while i < len(s):
    ch = s[i]
    if ch == "a":
        na += 1
    elif ch == "b":
        nb += 1
    elif ch == "n":
        nn += 1
    elif ch != " ":
        other += 1
    i += 1
print("text:", s)
print("a", "*" * na, na, sep=" ")
print("b", "*" * nb, nb, sep=" ")
print("n", "*" * nn, nn, sep=" ")
print("?", "*" * other, other, sep=" ")

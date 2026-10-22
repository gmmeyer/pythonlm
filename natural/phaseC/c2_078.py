pw = "go#9ers"
has_digit = False
has_symbol = False
for i in range(len(pw)):
    for k in range(10):
        if pw[i] == str(k):
            has_digit = True
    if pw[i] == "#" or pw[i] == "!" or pw[i] == "@":
        has_symbol = True
print("length ok:", len(pw) >= 6)
print("has digit:", has_digit)
print("has symbol:", has_symbol)

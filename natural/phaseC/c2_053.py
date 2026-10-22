text = "elite hacker"
out = ""
for i in range(len(text)):
    c = text[i]
    if c == "e":
        out += "3"
    elif c == "a":
        out += "4"
    elif c == "i":
        out += "1"
    elif c == "o":
        out += "0"
    else:
        out += c
print(out)

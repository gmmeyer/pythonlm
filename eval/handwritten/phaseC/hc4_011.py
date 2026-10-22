# Banner: frame a message with '+', '-' and '|', letters spaced apart.
msg = "BYTECODE"
spaced = ""
k = 0
while k < len(msg):
    spaced = spaced + msg[k]
    if k < len(msg) - 1:
        spaced = spaced + " "
    k += 1
inner = len(spaced) + 4
edge = "+" + "-" * inner + "+"
blank = "|" + " " * inner + "|"
print(edge)
print(blank)
print("|  " + spaced + "  |")
print(blank)
print(edge)
print("letters:", len(msg), "width:", len(edge), sep=" ")

msg = "GRAND OPENING"
width = 25
pad = (width - len(msg)) // 2
extra = width - len(msg) - pad
print("~" * (width + 2))
print("|" + " " * pad + msg + " " * extra + "|")
print("|" + " " * width + "|")
sub = "sat 10am"
p2 = (width - len(sub)) // 2
print("|" + " " * p2 + sub + " " * (width - len(sub) - p2) + "|")
print("~" * (width + 2))

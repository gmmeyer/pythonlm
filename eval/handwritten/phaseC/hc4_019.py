# Vertical column chart of five values, drawn from the top level down.
a = 3
b = 6
c = 2
d = 5
e = 4
lv = 6
while lv >= 1:
    line = str(lv) + " |"
    if a >= lv:
        line += " ##"
    else:
        line += "   "
    if b >= lv:
        line += " ##"
    else:
        line += "   "
    if c >= lv:
        line += " ##"
    else:
        line += "   "
    if d >= lv:
        line += " ##"
    else:
        line += "   "
    if e >= lv:
        line += " ##"
    else:
        line += "   "
    print(line)
    lv -= 1
print("  +" + "-" * 15)
print("    A  B  C  D  E")

home = 3
print("when it is " + str(home) + "am here:")
for off in range(-8, 11, 6):
    there = (home + off) % 24
    tag = "am"
    if there >= 12:
        tag = "pm"
    shown = there % 12
    if shown == 0:
        shown = 12
    sign = ""
    if off >= 0:
        sign = "+"
    print(f"  {sign}{off}h -> {shown}{tag}")

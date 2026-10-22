rows = "ABC"
for r in range(3):
    line = ""
    for seat in range(1, 5):
        line += rows[r] + str(seat) + " "
    print(line, end="")
    print("<- row", rows[r])
print("12 seats")

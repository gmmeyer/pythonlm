price = 50
for day in range(1, 9):
    change = (day * 7) % 11 - 5
    price += change
    if change > 0:
        arrow = "^"
    elif change < 0:
        arrow = "v"
    else:
        arrow = "-"
    print(day, price, arrow, sep="  ")

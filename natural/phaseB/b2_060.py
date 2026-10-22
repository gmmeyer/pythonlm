# nested loops: seating rows in a theater, stop at a full house
seats = 0
for row in range(1, 6):
    for col in range(1, 7):
        if (row + col) % 4 == 0:
            continue
        seats += 1
        if seats == 20:
            break
print(seats)

# speeding fines: 5 over is a warning, 6-20 over is 50, above that 150
limit = 60
for speed in range(55, 100, 8):
    over = speed - limit
    if over <= 5:
        fine = 0
    elif over <= 20:
        fine = 50
    else:
        fine = 150
    print(fine)

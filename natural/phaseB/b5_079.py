# ways to pay 30 with tens, fives and ones
ways = 0
for tens in range(4):
    for fives in range(7):
        if tens * 10 + fives * 5 <= 30:
            ways += 1
print(ways)

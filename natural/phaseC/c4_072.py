minutes = 0
for coin in range(1, 5):
    minutes += coin * 15
    print("coin", coin, "-> total", minutes, "min")
while minutes > 0:
    minutes -= 45
    if minutes > 0:
        print(minutes, "min left")
print("meter expired")

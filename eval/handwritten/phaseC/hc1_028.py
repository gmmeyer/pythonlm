paid = 0
minutes = 0
coins = 0
while minutes < 90:
    coins += 1
    paid += 25
    minutes += 20
print("coins inserted:", coins)
print(f"paid {paid} cents for {minutes} minutes")
extra = minutes - 90
if extra > 0:
    print("bonus time:", extra, "min")

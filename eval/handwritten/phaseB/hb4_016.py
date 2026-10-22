# A water tank with a pump. Households draw water every hour, more in
# the morning and evening rush. The pump turns on when the level falls
# below 30 and off once it passes 80. The pump adds 12 per hour.
level = 50
pump = False
starts = 0
print("water tank")
for hour in range(5, 21):
    if 6 <= hour <= 8 or 18 <= hour <= 20:
        use = 9
    elif hour < 6:
        use = 2
    else:
        use = 5
    level -= use
    if pump:
        level += 12
    if not pump and level < 30:
        pump = True
        starts += 1
        print("pump on at hour")
        print(hour)
    elif pump and level > 80:
        pump = False
        print("pump off")
    if hour % 4 == 0:
        print(level)
print("pump starts")
print(starts)
print(pump)

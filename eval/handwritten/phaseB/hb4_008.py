# An elevator in a nine-floor building. Each batch of requests is a number
# whose digits (lowest first) are the floors to visit. The car moves one
# floor per tick and spends one tick with the doors open at each stop.
floor = 1
ticks = 0
travelled = 0
print("elevator online")
for batch in range(2):
    if batch == 0:
        requests = 729
    else:
        requests = 418
    while requests > 0:
        target = requests % 10
        requests //= 10
        print("heading to")
        print(target)
        while floor != target:
            if floor < target:
                floor += 1
            else:
                floor -= 1
            ticks += 1
            travelled += 1
        ticks += 1
print("floors travelled")
print(travelled)
print("ticks used")
print(ticks)
print(floor == 4)

# Tortoise and hare race to 60. The tortoise moves 3 every tick. The hare
# moves 8, but whenever it is 15 or more ahead it naps for 4 ticks.
tortoise = 0
hare = 0
nap = 0
tick = 0
print("race start")
while tortoise < 60 and hare < 60:
    tick += 1
    tortoise += 3
    if nap > 0:
        nap -= 1
        if nap == 0:
            print("hare wakes up")
    else:
        hare += 8
        if hare - tortoise >= 15:
            nap = 4
            print("hare naps")
    if tick % 3 == 0:
        print(hare - tortoise)
if hare >= 60 and tortoise >= 60:
    print("photo finish")
elif hare >= 60:
    print("hare wins")
else:
    print("tortoise wins")
print(tick)

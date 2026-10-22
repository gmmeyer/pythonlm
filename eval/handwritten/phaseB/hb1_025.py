rent = 950
for roommates in range(2, 6):
    share = rent // roommates
    leftover = rent % roommates
    if leftover == 0:
        print("splits evenly")
    else:
        print(leftover)
    print(share)

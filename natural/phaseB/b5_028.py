# gambler starts with 10 and bets 1 per flip; stops at 0, 20 or 25 flips
x = 3
money = 10
flips = 0
while 0 < money < 20 and flips < 25:
    x = (x * 13 + 7) % 64
    if x % 2 == 0:
        money += 1
    else:
        money -= 1
    flips += 1
print(money)
print(flips)

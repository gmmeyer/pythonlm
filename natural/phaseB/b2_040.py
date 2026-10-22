# game: collect coins, every 5th is a bonus coin worth extra
coins = 0
value = 0
for i in range(1, 21):
    if i % 5 == 0:
        value += 10
    elif i % 2 == 0:
        value += 2
    else:
        value += 1
    coins += 1
print(coins)
print(value)

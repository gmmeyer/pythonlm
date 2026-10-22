# two players roll (fake dice), whoever goes first swaps each turn
seed = 5
first = 1
second = 2
p1 = p2 = 0
for turn in range(6):
    seed = (seed * 7 + 3) % 11
    roll = seed % 6 + 1
    if roll >= 4:
        if first == 1:
            p1 += roll
        else:
            p2 += roll
    first, second = second, first
print(p1)
print(p2)
print(p1 > p2)

# race to 20 points: players take turns drawing 1..6 from an LCG
x = 5
a = 0
b = 0
turn = 0
while a < 20 and b < 20:
    x = (x * 21 + 5) % 32
    roll = x % 6 + 1
    if turn % 2 == 0:
        a += roll
    else:
        b += roll
    turn += 1
print(turn)
if a > b:
    print("A wins")
else:
    print("B wins")

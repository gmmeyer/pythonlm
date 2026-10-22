# Lights out with three lamps stored as bits of a number (lamp 1 = 1,
# lamp 2 = 2, lamp 3 = 4). Button 1 toggles lamps 1 and 2, button 2 toggles
# all three, button 3 toggles lamps 2 and 3. Presses come from digits.
state = 5
darks = 0
print("lights out")
for batch in range(3):
    if batch == 0:
        presses = 213
    elif batch == 1:
        presses = 312
    else:
        presses = 331
    while presses > 0:
        b = presses % 10
        presses //= 10
        if b <= 2:
            if state % 2 == 1:
                state -= 1
            else:
                state += 1
        if state // 2 % 2 == 1:
            state -= 2
        else:
            state += 2
        if b >= 2:
            if state // 4 % 2 == 1:
                state -= 4
            else:
                state += 4
        print(state)
        if state == 0:
            darks += 1
            print("all dark")
print("times dark")
print(darks)

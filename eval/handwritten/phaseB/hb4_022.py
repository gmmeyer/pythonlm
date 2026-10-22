# A keypad lock with the code 3-1-4. Key presses arrive as digits of a few
# numbers (lowest digit first). The lock remembers how much of the code has
# matched; a wrong key resets it. Three wrong keys in a row lock the pad for
# the next two presses.
stage = 0
wrong_streak = 0
lockout = 0
opened = 0
print("keypad armed")
for batch in range(4):
    if batch == 0:
        keys = 314
    elif batch == 1:
        keys = 413
    elif batch == 2:
        keys = 777
    else:
        keys = 413
    while keys > 0:
        k = keys % 10
        keys //= 10
        if lockout > 0:
            lockout -= 1
            print("locked out")
            continue
        if (stage == 0 and k == 3) or (stage == 1 and k == 1) or (stage == 2 and k == 4):
            stage += 1
            wrong_streak = 0
        else:
            wrong_streak += 1
            if k == 3:
                stage = 1
            else:
                stage = 0
            if wrong_streak == 3:
                lockout = 2
                wrong_streak = 0
                print("too many errors")
        if stage == 3:
            opened += 1
            stage = 0
            print("door opens")
print("times opened")
print(opened)
print(stage)

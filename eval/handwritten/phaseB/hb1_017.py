correct = 472
guess = 400
tries = 0
locked = False
while guess != correct:
    tries += 1
    if tries > 3:
        locked = True
        break
    guess += 36
print(tries)
print(locked)
if not locked:
    print("welcome back")
else:
    print("account locked")

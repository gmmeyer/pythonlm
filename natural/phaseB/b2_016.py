# door lock: three wrong codes lock the door
attempts = 0
locked = False
code = 7
guess = 2
while not locked:
    if guess == code:
        print("open")
        break
    attempts += 1
    guess += 2
    if attempts == 3:
        locked = True
if locked:
    print("locked")
print(attempts)

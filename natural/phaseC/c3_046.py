secret = "tiger"
attempt = 0
solved = False
while attempt < 3 and not solved:
    attempt += 1
    if attempt == 1:
        guess = "lion"
    elif attempt == 2:
        guess = "tiger"
    else:
        guess = "bear"
    if guess == secret:
        print("Attempt", attempt, "correct!")
        solved = True
    else:
        print("Attempt", attempt, "wrong:", guess)

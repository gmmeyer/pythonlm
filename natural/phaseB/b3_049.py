lo = 0
hi = 100
guess = 0
target = 37
while lo <= hi:
    guess = (lo + hi) // 2
    print(guess)
    if guess == target:
        break
    elif guess < target:
        lo = guess + 1
    else:
        hi = guess - 1

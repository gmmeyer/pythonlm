# how many guesses does it take to find 700 between 1 and 999?
target = 700
lo = 1
hi = 999
guesses = 0
while True:
    guess = (lo + hi) // 2
    guesses += 1
    if guess == target:
        break
    if guess < target:
        lo = guess + 1
    else:
        hi = guess - 1
print(guesses)

# guessing game
secret = "tulip"
guess = "rose"
tries = 0
while guess != secret:
    tries += 1
    print("try", tries, "guess:", guess)
    if tries == 1:
        guess = "daisy"
    elif tries == 2:
        guess = "lily"
    else:
        guess = "tulip"
print("found", secret, "after", tries, "wrong guesses")

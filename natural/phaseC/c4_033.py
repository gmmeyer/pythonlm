pin = "4821"
tries = 0
guess = "1111"
while tries < 3 and guess != pin:
    tries += 1
    if tries == 3:
        guess = "4821"
    print("try", tries, "guess", guess)
if guess == pin:
    print("access granted after", tries, "tries")
else:
    print("account locked")

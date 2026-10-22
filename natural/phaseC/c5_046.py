# hangman board with spaces between the slots
secret = "rocket"
guess = "e"
for i in range(len(secret)):
    if secret[i] == guess:
        print(guess, end=" ")
    else:
        print("_", end=" ")
print()
print(len(secret), "letters")

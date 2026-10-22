secret = "planet"
guess = "a"
shown = ""
for i in range(len(secret)):
    if secret[i] == guess:
        shown += guess
    else:
        shown += "_"
print(shown)

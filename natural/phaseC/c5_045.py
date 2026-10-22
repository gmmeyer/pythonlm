secret = "planet"
guesses = "aetnl"
shown = "_" * len(secret)
for k in range(len(guesses)):
    g = guesses[k]
    new = ""
    for i in range(len(secret)):
        if secret[i] == g:
            new += g
        else:
            new += shown[i]
    shown = new
    print(g, "->", shown)

secret = "moon"
guesses = "nmxo"
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
    done = True
    for i in range(len(shown)):
        if shown[i] == "_":
            done = False
    print(shown)
    if done:
        print("you win after", k + 1, "guesses")
        break

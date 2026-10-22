secret = "kiwi"
guesses = "zikw"
lives = 3
shown = "____"
for k in range(len(guesses)):
    g = guesses[k]
    hit = False
    new = ""
    for i in range(len(secret)):
        if secret[i] == g:
            new += g
            hit = True
        else:
            new += shown[i]
    shown = new
    if not hit:
        lives -= 1
    print(f"guess {g}: {shown} lives={lives}")

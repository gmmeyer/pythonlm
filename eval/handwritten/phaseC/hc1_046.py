seed = 7
me = 0
you = 0
for rnd in range(1, 6):
    seed = (seed * 13 + 5) % 31
    a = seed % 6 + 1
    seed = (seed * 13 + 5) % 31
    b = seed % 6 + 1
    if a > b:
        me += 1
        winner = "me"
    elif b > a:
        you += 1
        winner = "you"
    else:
        winner = "tie"
    print(f"round {rnd}: {a} vs {b}, {winner}")
print("final", str(me) + "-" + str(you))

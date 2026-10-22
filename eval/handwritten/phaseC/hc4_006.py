# A tiny text adventure that plays itself; the turn counter picks moves.
room = "hall"
gold = 0
keys = 0
turn = 1
while turn <= 9:
    if room == "hall":
        if turn % 3 == 0:
            room = "vault"
            msg = "a heavy door opens"
        else:
            room = "cellar"
            msg = "stairs lead down"
    elif room == "cellar":
        keys += 1
        room = "hall"
        msg = "found a key"
    elif room == "vault":
        if keys > 0:
            keys -= 1
            gold += 25
            msg = "unlocked a chest"
        else:
            msg = "the chest is locked"
        room = "hall"
    print(f"turn {turn}: {msg}")
    print("   now in the", room)
    turn += 1
print("gold:", gold, "keys:", keys)

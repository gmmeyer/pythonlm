gold = 30
sword = 25
potion = 8
print("Welcome to the shop. You have", gold, "gold.")
if gold >= sword:
    gold -= sword
    print("You buy the sword. Gold left:", gold)
if gold >= potion:
    gold -= potion
    print("You buy a potion. Gold left:", gold)
else:
    print("Not enough gold for a potion.")

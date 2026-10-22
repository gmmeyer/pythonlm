# A treasure hunt driven by the generator x = (x * 7 + 3) % 101.
# Low draws are traps, middle draws are empty rooms, higher draws are
# gold and the highest are healing potions.
x = 17
gold = 0
health = 10
turn = 0
print("treasure hunt")
while health > 0 and turn < 20:
    turn += 1
    x = (x * 7 + 3) % 101
    if x < 20:
        health -= 3
        print("trap")
    elif x < 60:
        print("empty room")
    elif x < 90:
        gold += x // 10
        print("gold")
    else:
        health += 2
        print("potion")
print("turns, gold, health")
print(turn)
print(gold)
print(health)

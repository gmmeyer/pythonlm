hp = 20
room = 0
while hp > 0 and room < 5:
    room += 1
    if room % 2 == 1:
        hp -= 6
        print("Room", room, "trap! hp is", hp)
    else:
        hp += 3
        print("Room", room, "potion! hp is", hp)
if hp > 0:
    print("You survived with", hp, "hp")
else:
    print("You died in room", room)

has_key = False
room = 1
turns = 0
while room != 4 and turns < 10:
    turns += 1
    if room == 1:
        print("A locked door blocks the way.")
        room = 2
    elif room == 2:
        print("You find a key under a rug.")
        has_key = True
        room = 3
    elif room == 3:
        if has_key:
            print("The key fits! You open the door.")
            room = 4
        else:
            print("The door will not budge.")
print("Turns taken:", turns)

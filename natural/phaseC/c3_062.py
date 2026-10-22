room = 1
choice = 2
if room == 1:
    print("You are in a hall with two doors.")
    if choice == 1:
        print("Door 1 leads to a dragon. Run!")
        room = 3
    else:
        print("Door 2 leads to a garden.")
        room = 2
if room == 2:
    print("A gardener hands you a key.")
elif room == 3:
    print("The dragon is asleep.")
print("Room number:", room)

# bus every 3 minutes, train every 5
for minute in range(1, 16):
    bus = minute % 3 == 0
    train = minute % 5 == 0
    if bus and train:
        print("both arrive")
    elif bus:
        print("bus")
    elif train:
        print("train")
    else:
        pass   # nothing pulls in this minute

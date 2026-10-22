for k in range(3):
    if k == 0:
        name = "Charles"
        thing = "bike"
    elif k == 1:
        name = "Mia"
        thing = "lunchbox"
    else:
        name = "James"
        thing = "keys"
    if name[-1] == "s":
        owner = name + "'"
    else:
        owner = name + "'s"
    print(owner, thing)

for n in range(7, 12):
    name = "item" + str(n)
    nxt = "item" + str(n + 1)
    print(name, "<", nxt, "is", name < nxt)

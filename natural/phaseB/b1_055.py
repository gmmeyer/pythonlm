# which residues mod 7 are perfect squares?
for a in range(1, 7):
    found = False
    for x in range(1, 7):
        if x * x % 7 == a:
            found = True
    print(found)

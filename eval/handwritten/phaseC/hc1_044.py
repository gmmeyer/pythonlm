stamps = 0
for visit in range(1, 13):
    stamps += 1
    if stamps == 10:
        print("visit", visit, "-> FREE COFFEE")
        stamps = 0
        continue
    if visit % 3 == 0:
        card = "o" * stamps + "." * (10 - stamps)
        print("visit", visit, "card", card)
print("stamps now:", stamps)

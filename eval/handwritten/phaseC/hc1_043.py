w1 = "summer"
w2 = "road"
w3 = "trip"
tag = "#" + w1 + w2 + w3
print(tag)
print("chars:", len(tag))
if len(tag) > 12:
    short = "#" + w1[0] + w2[0] + w3[0]
    print("short version:", short)
print(tag + " " + "#" + w3 + str(len(w3)))

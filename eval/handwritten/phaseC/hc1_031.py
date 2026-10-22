w1 = "as"
w2 = "soon"
w3 = "as"
w4 = "possible"
acr = w1[0] + w2[0] + w3[0] + w4[0]
print(w1, w2, w3, w4, sep=" ", end=" = ")
print(acr)
if acr == "asap":
    print("classic")
x1 = "laughing"
x2 = "out"
x3 = "loud"
other = x1[0] + x2[0] + x3[0]
print(f"{x1} {x2} {x3} = {other}")
print("both together:", acr + "/" + other, len(acr + other))

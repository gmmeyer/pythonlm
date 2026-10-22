# bounded countdown with early exit
t = 15
while t > 0:
    t -= 2
    if t == 7:
        print("halfway")
    if t < 3:
        print("almost")
        break
print(t)

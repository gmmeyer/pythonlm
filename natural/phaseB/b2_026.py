temp = 30
cooling = True
steps = 0
while cooling:
    temp -= 4
    steps += 1
    if temp <= 18:
        cooling = False
print(temp)
print(steps)

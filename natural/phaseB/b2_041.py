power = 1
for i in range(12):
    if power > 300:
        print("overflow guard")
        break
    power *= 2
print(power)

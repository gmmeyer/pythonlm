moisture = 60
waterings = 0
for hour in range(36):
    moisture -= 3
    if moisture < 30:
        moisture += 25
        waterings += 1
print(moisture)
print(waterings)

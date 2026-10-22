battery = 64
for hour in range(1, 13):
    if battery < 20:
        battery += 35
        print("charging")
    else:
        battery -= 12
    if battery > 100:
        battery = 100
print(battery)

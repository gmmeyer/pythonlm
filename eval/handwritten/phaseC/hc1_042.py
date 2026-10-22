tank = 45
best = 0
for trip in range(3):
    if trip == 0:
        km = 610
    elif trip == 1:
        km = 585
    else:
        km = 640
    whole = km // tank
    rem = km % tank
    tenth = rem * 10 // tank
    print(f"tank {trip + 1}: {km} km, {whole}.{tenth} km/l")
    if km > best:
        best = km
print("best tank:", best, "km")

total = 0
km = 40
print("day", "km", "total", sep="\t")
for day in range(1, 7):
    total += km
    print(day, km, total, sep="\t")
    km = km + day * 5

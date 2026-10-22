# Calendar for February 2027: 28 days, and the 1st is a Monday,
# so the month fills exactly four week rows.
print("   February 2027")
print("Mo Tu We Th Fr Sa Su")
for week in range(4):
    line = ""
    for wd in range(1, 8):
        day = week * 7 + wd
        s = str(day)
        if day < 10:
            s = " " + s
        line = line + s + " "
    print(line)
print("weeks: 4", "days: 28", sep=", ")

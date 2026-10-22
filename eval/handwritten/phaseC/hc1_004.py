days = "MTWTFSS"
first = 27
month_len = 30
header = ""
for d in range(7):
    header += "  " + days[d]
print(header)
row = ""
day = first
for d in range(7):
    if day < 10:
        row += "  " + str(day)
    else:
        row += " " + str(day)
    day += 1
    if day > month_len:
        day = 1
print(row)
print("week starting the " + str(first) + "th")

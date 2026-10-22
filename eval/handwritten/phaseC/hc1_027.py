days = "SMTWTFS"
hi = -99
lo = 99
hi_day = ""
temp = 14
for d in range(7):
    temp = temp + (d * 5) % 7 - 3
    if temp > hi:
        hi = temp
        hi_day = days[d]
    if temp < lo:
        lo = temp
    print(days[d] + ":" + str(temp), end=" ")
print()
print(f"high {hi} on {hi_day}, low {lo}")

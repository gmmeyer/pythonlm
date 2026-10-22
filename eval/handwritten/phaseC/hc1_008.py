print("hours", "minutes", sep=" | ")
for h in range(1, 4):
    mins = h * 60
    print(f"{h} h = {mins} min")
total_min = 135
hrs = total_min // 60
rest = total_min % 60
print(f"{total_min} minutes is {hrs} h {rest} min")
quarter = 15
print("a quarter hour is", quarter, "min", end=", ")
print(f"three of them is {quarter * 3}")

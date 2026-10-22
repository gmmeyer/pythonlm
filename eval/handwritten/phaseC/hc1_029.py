total = 0
age = 2
for k in range(7):
    if age < 5:
        kind = "free"
        cost = 0
    elif age < 13:
        kind = "child"
        cost = 7
    elif age >= 65:
        kind = "senior"
        cost = 8
    else:
        kind = "adult"
        cost = 12
    total += cost
    print(f"age {age}: {kind} ({cost})")
    age = age + age // 2 + 3
print("party total", total, sep=" -> ")

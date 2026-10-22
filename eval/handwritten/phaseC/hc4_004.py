# Horizontal bar chart of five monthly sales figures.
# One '=' per 10 units; a trailing '-' for a remainder of 5 or more.
jan = 42
feb = 75
mar = 18
apr = 96
may = 60
print("Sales by month")
print("-" * 20)
best = 0
best_name = "?"
m = 0
while m < 5:
    if m == 0:
        name = "Jan"
        v = jan
    elif m == 1:
        name = "Feb"
        v = feb
    elif m == 2:
        name = "Mar"
        v = mar
    elif m == 3:
        name = "Apr"
        v = apr
    else:
        name = "May"
        v = may
    bar = "=" * (v // 10)
    if v % 10 >= 5:
        bar = bar + "-"
    print(name, "|" + bar, v)
    if v > best:
        best = v
        best_name = name
    m += 1
total = jan + feb + mar + apr + may
print("-" * 20)
print("total", total, sep=": ")
print("best", best_name, sep=": ")

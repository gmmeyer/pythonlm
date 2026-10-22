cents = 87
print("change due:", cents, "cents")
q = cents // 25
cents = cents % 25
d = cents // 10
cents %= 10
n = cents // 5
p = cents % 5
print(f"quarters: {q}")
print(f"dimes:    {d}")
print(f"nickels:  {n}")
print(f"pennies:  {p}")
print("coins total", q + d + n + p, sep=" = ")

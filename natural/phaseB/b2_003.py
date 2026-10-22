# population growth capped at a limit
pop = 12
cap = 200
years = 0
while pop < cap:
    pop = pop * 3 // 2 + 2
    if pop > cap:
        pop = cap
    years += 1
print(years)
print(pop)
print(pop == cap)

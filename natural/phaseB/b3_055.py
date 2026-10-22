# population doubling every step until over 500
pop = 8
years = 0
while pop <= 500:
    pop *= 2
    years += 1
    print(pop)
print(years)

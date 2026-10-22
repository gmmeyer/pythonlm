# fish pond: population grows, but fishing removes some
fish = 20
year = 0
for year in range(1, 11):
    fish += fish // 4
    if fish > 60:
        fish -= 25
    elif fish > 40:
        fish -= 10
print(fish)
print(year)

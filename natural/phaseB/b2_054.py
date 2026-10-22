# interest doubling time
money = 100
years = 0
while money < 200:
    money += money * 7 // 100
    years += 1
print(years)
print(money)

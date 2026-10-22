# garage: first hour is 3, then 2 for every started half hour
minutes = 135
first_hour = 3
extra = minutes - 60
halves = (extra + 29) // 30
fee = first_hour + 2 * halves
print("parking fee")
print(fee)

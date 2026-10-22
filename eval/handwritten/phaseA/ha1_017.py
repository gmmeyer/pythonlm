dep_h = 22
dep_m = 40
travel = 95
m = dep_m + travel
arr_h = (dep_h + m // 60) % 24
arr_m = m % 60
print(arr_h)
print(arr_m)

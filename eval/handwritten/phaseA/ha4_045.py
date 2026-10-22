# A reservoir, measured in thousands of cubic meters, week by week.
# Rain flows in, the town draws 70 a week, and evaporation takes
# 1 unit for every 25 stored (twice that in a hot week).

level = 420
town = 70
lost = 0

print("Week 1")
rain = 55
evap = level // 25
level += rain - town - evap
lost += evap
print(level)

print("Week 2: dry")
rain = 0
evap = level // 25
level += rain - town - evap
lost += evap
print(level)

print("Week 3: dry and hot")
evap = level // 25 * 2
level += rain - town - evap
lost += evap
print(level)

print("Week 4: storm")
rain = 240
evap = level // 25
level += rain - town - evap
lost += evap
print(level)

print("Week 5: rationing")
# the town cuts its use by a quarter
town = town * 3 // 4
rain = 30
evap = level // 25
level += rain - town - evap
lost += evap
print(town)
print(level)

print("Week 6")
rain = 12
evap = level // 25
level += rain - town - evap
lost += evap
print(level)

print("--- report ---")
print(level - 420)
print(lost)
# weeks left if no more rain falls
print(level // (town + level // 25))

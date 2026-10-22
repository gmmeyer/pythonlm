# monthly budget, rough numbers in tens of dollars
income = 360
rent = 160
utilities = 18
phone = 6
groceries = 55
transport = 22
fun = 30
savings_goal = 80

spent = rent + utilities + phone
spent += groceries
spent += transport
spent += fun
print("spent")
print(spent)

left = income - spent
print("left over")
print(left)

gap = left - savings_goal
print("vs goal")
print(gap)

# spread the gap over the 4 weeks
per_week = gap // 4
print(per_week)
print(gap % 4)

# cut fun money in half and redo it
fun //= 2
spent = rent + utilities + phone + groceries + transport + fun
left = income - spent
print(left - savings_goal)

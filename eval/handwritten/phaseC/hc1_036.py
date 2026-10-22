income = 950
rent = 600
food = 210
spent = rent + food
left = income - spent
print(f"income {income}, spent {spent}")
if left < 0:
    print("over budget by", -left)
else:
    print("under budget by", left)
    fun = left // 2
    save = left - fun
    print("fun money:", fun, "| savings:", save)
weekly = food // 4
print("food per week ~", weekly, sep="")

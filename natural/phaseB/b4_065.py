speed = 78
limit = 60
over = speed - limit
if over <= 0:
    fine = 0
elif over <= 10:
    fine = 20
elif over <= 20:
    fine = 50
else:
    fine = 100
print(fine)

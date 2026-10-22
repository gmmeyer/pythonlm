# raise of 3 every third year of service, starting salary 40
salary = 40
for years in range(1, 13):
    if years % 3 == 0:
        salary = salary + 3
print(salary)
if salary >= 50:
    print("senior band")
else:
    print("junior band")

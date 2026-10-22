# weekly wage report
rate = 15
mon = 8
tue = 6
wed = 9
total_hours = mon + tue + wed
pay = total_hours * rate
print(f"hours worked: {total_hours}")
print(f"rate per hour: {rate}")
print(f"gross pay: {pay}")
overtime = 0
if total_hours > 20:
    overtime = (total_hours - 20) * rate // 2
print(f"overtime bonus: {overtime}")
print(f"total: {pay + overtime}")

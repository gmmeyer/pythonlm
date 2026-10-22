# a meeting that starts at 9:50 and runs 135 minutes
start_hour = 9
start_min = 50
duration = 135
total = start_hour * 60 + start_min + duration
end_hour = total // 60 % 24
end_min = total % 60
print("ends at hour:")
print(end_hour)
print("minute:")
print(end_min)

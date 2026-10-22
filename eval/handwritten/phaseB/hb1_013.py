tank = 0
size = 50
minute = 0
while tank < size:
    minute += 1
    tank += 9
    if minute % 3 == 0:
        tank -= 4      # the leak catches up every third minute
    print(tank)
print(minute)
print(tank - size)

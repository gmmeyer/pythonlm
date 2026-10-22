# water level sensor with alarm flag
level = 10
alarm = False
for hr in range(12):
    level += 7 - hr
    if level > 40 or level < 0:
        alarm = True
print(level)
print(alarm)

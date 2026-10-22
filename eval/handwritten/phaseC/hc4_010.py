# A 30-unit ruler: '|' every 10, ':' every 5, '.' for the rest,
# with numeric labels placed under the long ticks.
length = 30
ticks = ""
for x in range(length + 1):
    if x % 10 == 0:
        ticks += "|"
    elif x % 5 == 0:
        ticks += ":"
    else:
        ticks += "."
print(ticks)
labels = ""
x = 0
while x <= length:
    s = str(x)
    labels = labels + s + " " * (10 - len(s))
    x += 10
print(labels)
print("units:", length, "ticks:", len(ticks))

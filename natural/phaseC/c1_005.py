# a month grid that starts on day 3 of the week
start = 3
days = 30
print("Su Mo Tu We Th Fr Sa")
col = 0
for blank in range(start):
    print("  ", end=" ")
    col += 1
for d in range(1, days + 1):
    if d < 10:
        print(" ", end="")
    print(d, end=" ")
    col += 1
    if col == 7:
        print()
        col = 0
if col != 0:
    print()

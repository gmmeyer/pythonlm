floor = 1
dest = 8
while True:
    floor += 1
    if floor == 4:
        continue   # no 4th floor button in this building
    print(floor)
    if floor == dest:
        print("doors opening")
        break

# back down to the lobby, express
for f in range(dest, 0, -3):
    print(f)

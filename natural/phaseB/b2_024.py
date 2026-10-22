# elevator visiting a list of requested floors, one by one
floor = 0
travelled = 0
for request in range(2, 11, 3):
    while floor < request:
        floor += 1
        travelled += 1
print(floor)
for request in range(8, 0, -4):
    while floor > request:
        floor -= 1
        travelled += 1
print(floor)
print(travelled)

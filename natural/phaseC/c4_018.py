floor = 1
goal = 4
direction = "up"
while floor != goal:
    print("floor", floor, "going", direction)
    floor += 1
print("arrived at floor", floor, "- doors open")
direction = "down"
goal = 2
while floor != goal:
    print("floor", floor, "going", direction)
    floor -= 1
print("arrived at floor", floor, "- doors open")

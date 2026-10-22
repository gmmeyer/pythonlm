# elevator moving between floors
floor = 1
target = 7
moves = 0
while floor != target:
    if floor < target:
        floor += 1
    else:
        floor -= 1
    moves += 1
print(moves)
target = 3
while floor != target:
    if floor < target:
        floor += 1
    else:
        floor -= 1
    moves += 1
print(moves)
print(floor)

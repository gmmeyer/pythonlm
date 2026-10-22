# two pointers walk toward each other until they meet
lo = 0
hi = 100
moves = 0
while lo < hi:
    if moves % 2 == 0:
        lo += 3
    else:
        hi -= 5
    moves += 1
print(lo)
print(hi)
print(moves)

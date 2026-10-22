# squares as sums of odd numbers
sq = 0
odd = 1
for i in range(1, 13):
    sq += odd
    odd += 2
    print(sq)

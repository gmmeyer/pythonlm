# a ball dropped from 200 loses half its height each bounce; stop below 5
height = 200
bounces = 0
distance = 200
while height >= 10:
    height //= 2
    bounces += 1
    distance += 2 * height
print(bounces)
print(height)
print(distance)

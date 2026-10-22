# Nicomachus: sum of cubes equals the square of the triangular number
cubes = 0
tri = 0
for i in range(1, 7):
    cubes += i * i * i
    tri += i
print(cubes)
print(tri * tri)
print(cubes == tri * tri)

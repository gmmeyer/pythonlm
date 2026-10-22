students = 29
per_row = 6
# ceiling division with the negate trick
rows = -(-students // per_row)
print(rows)
empty = rows * per_row - students
print(empty)

x = 5
for v in range(-1, 8, 3):
    print(f"{v}: {0 <= v < x} {v == x - 3} {-v}")
lo = 2
hi = 2
print(f"{lo <= hi <= lo} {lo < hi < 9} {lo == hi != 3}")

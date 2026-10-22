low = 999
high = -999
x = 17
for i in range(8):
    x = (x * 7 + 3) % 41
    if x < low:
        low = x
    if x > high:
        high = x
    print(x, end=" ")
print()
print(f"low {low}, high {high}")

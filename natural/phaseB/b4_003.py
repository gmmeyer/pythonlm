x = 7
smallest = 999
largest = -999
for i in range(10):
    x = (x * 5 + 3) % 101
    if x < smallest:
        smallest = x
    if x > largest:
        largest = x
print(smallest)
print(largest)

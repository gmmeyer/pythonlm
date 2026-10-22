# multiples of 7 up to 60, with a marker after the first group of three
count = 0
for n in range(7, 61, 7):
    print(n)
    count += 1
    if count == 3:
        print("--")

# stop at the first multiple of 9 that is also a multiple of 4
for n in range(1, 100):
    if n % 9 == 0 and n % 4 == 0:
        print(n)
        break
print("done")

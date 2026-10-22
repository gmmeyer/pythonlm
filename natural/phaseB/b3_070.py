# smallest number that leaves remainder 2 mod 3, 3 mod 5, 2 mod 7
n = 0
while not (n % 3 == 2 and n % 5 == 3 and n % 7 == 2):
    n += 1
print(n)

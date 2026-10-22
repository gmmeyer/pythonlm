# two-digit numbers where digit product equals digit sum
for n in range(10, 50):
    a = n // 10
    b = n % 10
    if a * b == a + b:
        print(n)

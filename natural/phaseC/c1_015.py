# countdown with messages
for n in range(10, -1, -1):
    if n == 0:
        print("Blast off!")
    elif n <= 3:
        print(n, "- engines on")
    elif n % 5 == 0:
        print(n, "- checking systems")
    else:
        print(n)

password = "hunter2"
n = len(password)
if n < 6:
    print("Too short")
elif n < 10:
    print("OK length:", n)
else:
    print("Long and strong")

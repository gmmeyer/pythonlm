# every 3rd stop is express, every 5th is a terminal; both at once at stop 15
for stop in range(1, 16):
    if stop % 15 == 0:
        print("express terminal")
    elif stop % 5 == 0:
        print("terminal")
    elif stop % 3 == 0:
        print("express")

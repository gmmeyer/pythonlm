print("Celsius", "Fahrenheit", sep=" | ")
for c in range(-10, 41, 10):
    f = c * 9 // 5 + 32
    print(c, f, sep=" | ")

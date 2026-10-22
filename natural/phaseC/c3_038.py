print("Fahrenheit to Celsius")
for temp_f in range(-40, 101, 35):
    temp_c = (temp_f - 32) * 5 // 9
    print(temp_f, "F is about", temp_c, "C")

for score in range(66, 100, 8):
    if score >= 90:
        letter = "A"
    elif score >= 80:
        letter = "B"
    elif score >= 70:
        letter = "C"
    else:
        letter = "D"
    suffix = ""
    if score % 10 >= 7:
        suffix = "+"
    elif score % 10 <= 2:
        suffix = "-"
    print(score, letter + suffix)

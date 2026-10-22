name = "Jules"
score = 58
while score <= 100:
    if score >= 90:
        g = "A"
    elif score >= 80:
        g = "B"
    elif score >= 70:
        g = "C"
    elif score >= 60:
        g = "D"
    else:
        g = "F"
    print(name, "scored", score, "->", g)
    score += 11

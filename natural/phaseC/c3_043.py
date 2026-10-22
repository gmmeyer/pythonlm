pw1 = "abc"
pw2 = "letmein99"
pw3 = "correct horse"
for k in range(1, 4):
    if k == 1:
        pw = pw1
    elif k == 2:
        pw = pw2
    else:
        pw = pw3
    size = len(pw)
    if size < 6:
        verdict = "weak"
    elif size < 10:
        verdict = "fair"
    else:
        verdict = "strong"
    print(f"Password {k} has {size} characters: {verdict}")

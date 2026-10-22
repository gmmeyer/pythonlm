for place in range(1, 24, 2):
    last_digit = place % 10
    tens = place // 10 % 10
    if tens == 1:
        suf = "th"
    elif last_digit == 1:
        suf = "st"
    elif last_digit == 2:
        suf = "nd"
    elif last_digit == 3:
        suf = "rd"
    else:
        suf = "th"
    print(f"{place}{suf} place gets {200 - place * 8} pts")

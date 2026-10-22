# reading goal tracker
goal = 300
pages = 0
for day in range(1, 8):
    pages += 35 + day * 3
    if pages >= goal:
        status = "goal met"
    else:
        status = "keep going"
    print(f"day {day}: {pages} pages, {status}")

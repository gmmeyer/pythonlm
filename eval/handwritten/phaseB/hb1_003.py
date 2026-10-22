players = 23

# try a few team sizes and see what's left over
for per_team in range(3, 7):
    teams = players // per_team
    extra = players % per_team
    if extra == 0:
        print("even split")
    elif extra >= per_team - 1:
        print("one short team")
    else:
        print(extra)
    print(teams)

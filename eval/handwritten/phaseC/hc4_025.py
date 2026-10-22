# Tally marks for four teams: each full group of five is '||||/ '.
# The leader is tracked while the tallies are printed.
best = -1
leader = ""
all_votes = 0
for k in range(4):
    if k == 0:
        team = "reds  "
        votes = 13
    elif k == 1:
        team = "blues "
        votes = 7
    elif k == 2:
        team = "greens"
        votes = 21
    else:
        team = "golds "
        votes = 4
    groups = votes // 5
    rest = votes % 5
    marks = "||||/ " * groups + "|" * rest
    print(team, marks, sep=" : ")
    all_votes += votes
    if votes > best:
        best = votes
        leader = team
print("votes cast:", all_votes)
print("leader:", leader + "with", best)

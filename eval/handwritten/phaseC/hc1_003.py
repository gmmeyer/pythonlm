p1 = "ann"
p2 = "bo"
p3 = "cyd"
s1 = 12
s2 = 7
s3 = 15
print("PLAYER", "PTS", sep="\t")
print(p1, s1, sep="\t")
print(p2, s2, sep="\t")
print(p3, s3, sep="\t")
best = p1
top = s1
if s2 > top:
    best, top = p2, s2
if s3 > top:
    best, top = p3, s3
print("leader:", best, "with", top, "pts")
print("gap to last", top - s2, sep=" = ")

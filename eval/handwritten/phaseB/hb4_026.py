# A small epidemic in a town of 500 (susceptible, infected, recovered).
# New infections each day: (infected // 2 + 1) times (susceptible // 100),
# never more than the susceptible left. A fifth of the infected, plus one,
# recover each day.
s = 490
i = 10
r = 0
day = 0
print("epidemic")
while i > 0 and day < 16:
    day += 1
    new = (i // 2 + 1) * (s // 100)
    if new > s:
        new = s
    rec = i // 5 + 1
    s -= new
    i = i + new - rec
    r += rec
    print(i)
print("day, susceptible, recovered")
print(day)
print(s)
print(r)
print(s + i + r == 500)

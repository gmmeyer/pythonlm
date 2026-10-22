home = "Lions"
away = "Tigers"
h = 0
a = 0
for quarter in range(1, 5):
    h += quarter * 3 % 7 + 2
    a += quarter * 5 % 6 + 1
    print(f"Q{quarter}: {home} {h} - {away} {a}")
if h > a:
    print(f"{home} win by {h - a}")
elif a > h:
    print(f"{away} win by {a - h}")
else:
    print("tie game")

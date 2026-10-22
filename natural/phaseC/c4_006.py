ann = 0
bob = 0
for r in range(1, 6):
    ann += r % 3
    bob += (r * 2) % 4
    print(f"round {r}: Ann {ann}, Bob {bob}")
if ann > bob:
    print("Ann leads")
elif bob > ann:
    print("Bob leads")
else:
    print("tie game")

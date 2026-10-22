# Turn-based battle: a knight and a troll trade blows until one falls.
# The knight hits harder on even rounds; the troll regenerates a little.
knight_hp = 60
troll_hp = 75
round_no = 0
print("battle begins")
while knight_hp > 0 and troll_hp > 0:
    round_no += 1
    # knight attacks first
    if round_no % 2 == 0:
        dmg = 9
    else:
        dmg = 6
    troll_hp -= dmg
    if troll_hp <= 0:
        print("troll falls")
        break
    # troll regenerates 2 hp every third round
    if round_no % 3 == 0:
        troll_hp += 2
    # troll swings back
    knight_hp -= 5 + round_no % 4
    print(round_no)
    print(knight_hp)
    print(troll_hp)
print("rounds fought")
print(round_no)
print(knight_hp > 0)

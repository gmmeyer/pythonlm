hp = 10
hits = 0
while hp > 0:
    print("HP [" + "#" * hp + "." * (10 - hp) + "]", hp)
    hp -= 3
    hits += 1
print("defeated after", hits, "hits")

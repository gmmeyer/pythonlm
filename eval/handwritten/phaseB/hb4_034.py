# Hot potato in a circle: every third player is removed until one remains.
# Rather than tracking every seat, grow the circle one player at a time:
# the survivor's seat for n players is (survivor for n - 1 plus 3) % n.
survivor = 0
print("hot potato circle")
for n in range(2, 31):
    survivor = (survivor + 3) % n
    if n % 5 == 0:
        print("players")
        print(n)
        print(survivor + 1)
print("survivor seat for 30")
print(survivor + 1)
print(survivor + 1 > 15)

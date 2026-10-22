# Two meshed gears with 8 and 12 teeth. Each tick both turn by one tooth.
# We track the tooth under each gear's mark and count full turns, and we
# stop when both marks line up again at tooth 0.
small = 0
big = 0
small_turns = 0
big_turns = 0
ticks = 0
print("gear train")
while True:
    ticks += 1
    small = (small + 1) % 8
    big = (big + 1) % 12
    if small == 0:
        small_turns += 1
        print("small gear turn")
    if big == 0:
        big_turns += 1
        print("big gear turn")
    if small == 0 and big == 0:
        break
print(ticks)
print(small_turns)
print(big_turns)

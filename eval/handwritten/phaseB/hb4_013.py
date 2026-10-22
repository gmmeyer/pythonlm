# A frog crosses a pond of 20 lily pads, jumping 3 pads at a time.
# Pads whose number is a multiple of 4 are slippery, so the frog slides
# back one pad. Passing pad 20 means it crossed and starts a new lap.
pad = 0
laps = 0
slips = 0
jumps = 0
print("frog in the pond")
while laps < 2:
    jumps += 1
    pad += 3
    if pad > 20:
        laps += 1
        pad -= 21
        print("crossed the pond")
        print(jumps)
    elif pad % 4 == 0:
        pad -= 1
        slips += 1
        print("slip at")
        print(pad + 1)
print("slips")
print(slips)
print(pad)

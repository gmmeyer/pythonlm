# A juggler with three balls: red (57 g), green (63 g), blue (71 g).
# There are three slots: left hand, air, right hand. Each throw moves
# every ball one slot along: left -> air -> right -> left.
# Strain counts a tenth of the weight of each ball thrown up.

left = 57
air = 63
right = 71
strain = 0

print("Throw 1")
left, air, right = right, left, air
strain += air // 10
print(air)

print("Throw 2")
left, air, right = right, left, air
strain += air // 10
print(air)

print("Throw 3")
left, air, right = right, left, air
strain += air // 10
print(air)

print("Cross-hand trick")
# the hands trade balls; the air slot is empty for a moment
left, right = right, left
print(left)
print(right)

print("Throw 4")
left, air, right = right, left, air
strain += air // 10
print(air)

print("A club replaces the ball in the air")
air = 120

print("Throw 5")
left, air, right = right, left, air
strain += air // 10
print(air)

print("Throw 6")
left, air, right = right, left, air
strain += air // 10
print(air)

print("--- act over ---")
print(left)
print(right)
print(left - right)
print(strain)

# A cargo ship flies between space stations.
# Every leg burns 120 fuel plus 15 per crew member, and the crew
# breathes 3 units of oxygen per person per day.

fuel = 850
oxygen = 600
crew = 4

print("Leg 1: Earth to Luna")
days = 12
fuel -= 120 + crew * 15
oxygen -= crew * days * 3
print(fuel)
print(oxygen)

print("Luna station")
# fill half of the empty space in the 900 tank, take on a new crew member
fuel += (900 - fuel) // 2
crew += 1
oxygen += 150
print(fuel)
print(oxygen)

print("Leg 2: Luna to Mars")
days = 20
fuel -= 120 + crew * 15
oxygen -= crew * days * 3
print(fuel)
print(oxygen)

print("Leak!")
# the leak costs a sixth of the fuel
fuel -= fuel // 6
print(fuel)

print("Leg 3: Mars to Ceres")
# two crew members stay on Mars
days = 9
crew -= 2
fuel -= 120 + crew * 15
oxygen -= crew * days * 3
print(fuel)
print(oxygen)

print("--- arrival ---")
print(crew)
# days of air left for the remaining crew
print(oxygen // (crew * 3))
print(oxygen % (crew * 3))

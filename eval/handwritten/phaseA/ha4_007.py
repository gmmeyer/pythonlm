# A small football tournament: Lions, Hawks, Bears and Otters.
# A win is worth 3 points, a draw 1 point. We also keep goal difference.
# Every team plays every other team once, over three matchdays.

lions = hawks = bears = otters = 0
lions_gd = hawks_gd = bears_gd = otters_gd = 0

print("Matchday 1")
# Lions 2 - 1 Hawks
home = 2
away = 1
lions += 3
lions_gd += home - away
hawks_gd += away - home
# Bears 0 - 0 Otters
bears += 1
otters += 1

print("Matchday 2")
# Lions 1 - 1 Bears
lions += 1
bears += 1
# Hawks 3 - 0 Otters
home = 3
away = 0
hawks += 3
hawks_gd += home - away
otters_gd += away - home

print("Matchday 3")
# Lions 0 - 2 Otters
home = 0
away = 2
otters += 3
lions_gd += home - away
otters_gd += away - home
# Hawks 2 - 4 Bears
home = 2
away = 4
bears += 3
hawks_gd += home - away
bears_gd += away - home

print("--- table: points, then goal difference ---")
print("Lions")
print(lions)
print(lions_gd)
print("Hawks")
print(hawks)
print(hawks_gd)
print("Bears")
print(bears)
print(bears_gd)
print("Otters")
print(otters)
print(otters_gd)

# sort key: points * 100 + goal difference
print("--- sort keys ---")
print(lions * 100 + lions_gd)
print(hawks * 100 + hawks_gd)
print(bears * 100 + bears_gd)
print(otters * 100 + otters_gd)

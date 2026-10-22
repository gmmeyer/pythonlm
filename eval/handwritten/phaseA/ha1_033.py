# water in decilitres, goal is 2 litres
goal_dl = 20
glass_dl = 3
drunk = 0
drunk += glass_dl
drunk += glass_dl
drunk += 5    # big mug of tea
drunk += glass_dl
remaining = goal_dl - drunk
glasses_needed = (remaining + glass_dl - 1) // glass_dl
print(remaining)
print(glasses_needed)

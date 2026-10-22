# cooldown after each shot
cooldown = 0
shots = 0
for tick in range(25):
    if cooldown > 0:
        cooldown -= 1
    else:
        shots += 1
        cooldown = 3
print(shots)
print(cooldown)

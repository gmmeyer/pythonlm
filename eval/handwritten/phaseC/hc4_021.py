# Rocket launch log: a countdown with events, then the climb,
# where the exhaust flame grows longer every second.
t = 10
while t >= 0:
    note = ""
    if t == 8:
        note = " fuel pressurised"
    elif t == 5:
        note = " engines armed"
    elif t == 2:
        note = " ignition"
    print("T-" + str(t) + note)
    t -= 1
print("LIFTOFF")
alt = 0
for sec in range(1, 6):
    alt += sec * 40
    print("  /\\", "alt " + str(alt) + "m", sep="   ")
    print("  ||")
    print("  " + "v" * sec)
print("orbit in sight at", alt, "m")

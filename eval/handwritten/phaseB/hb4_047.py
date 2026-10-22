# A model rocket. After a countdown, the motor gives 14 of thrust for
# 5 ticks while gravity takes 10 each tick. Once it falls faster than 15
# the parachute opens and it drifts down at 4 per tick until it lands.
for t in range(3, 0, -1):
    print(t)
print("liftoff")
alt = 0
vel = 0
fuel = 5
tick = 0
chute = False
while tick < 30:
    tick += 1
    if fuel > 0:
        vel += 14
        fuel -= 1
    if chute:
        vel = -4
    else:
        vel -= 10
    alt += vel
    if alt <= 0:
        alt = 0
        print("landed")
        break
    if not chute and vel < -15:
        chute = True
        print("parachute")
    print(alt)
print(tick)

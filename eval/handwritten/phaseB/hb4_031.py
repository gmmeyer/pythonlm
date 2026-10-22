# A delivery drone flies three routes. Leg lengths are the digits of a
# number (lowest first). Each leg costs twice its length plus 3 for the
# takeoff. If a leg would leave less than 15 battery, the drone first goes
# home and recharges to 100.
battery = 100
recharges = 0
legs_done = 0
print("drone routes")
for route in range(3):
    if route == 0:
        legs = 978
    elif route == 1:
        legs = 465
    else:
        legs = 899
    while legs > 0:
        leg = legs % 10
        legs //= 10
        cost = leg * 2 + 3
        if battery - cost < 15:
            battery = 100
            recharges += 1
            print("recharge")
        battery -= cost
        legs_done += 1
        print(battery)
print("legs flown")
print(legs_done)
print(recharges)

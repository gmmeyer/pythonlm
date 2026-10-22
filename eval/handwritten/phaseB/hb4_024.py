# A bus drives a loop of 8 stops twice. At each stop a third of the riders
# get off, then some people want to board. The bus holds 12; anyone who
# does not fit is left behind at the stop.
riders = 0
left_behind = 0
boarded = 0
print("bus route")
for lap in range(2):
    for stop in range(8):
        off = riders // 3
        riders -= off
        want = (stop * 3 + lap) % 7 + 1
        room = 12 - riders
        if want > room:
            left_behind += want - room
            want = room
        riders += want
        boarded += want
    print("end of lap")
    print(riders)
print("boarded")
print(boarded)
print("left behind")
print(left_behind)

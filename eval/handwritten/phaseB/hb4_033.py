# A farmer's field over 18 days. Rain (a draw from x = (x * 7 + 3) % 101
# that is a multiple of 4) grows the crop by 3. On dry even days the farmer
# waters and the crop grows by 2. Dry odd days make it wilt by 1.
# The crop is harvested when it reaches 10 and replanted from 0.
x = 23
crop = 0
harvests = 0
print("farm diary")
for day in range(1, 19):
    x = (x * 7 + 3) % 101
    rain = x % 4 == 0
    if rain:
        crop += 3
    elif day % 2 == 0:
        crop += 2
    elif crop > 0:
        crop -= 1
    if crop >= 10:
        harvests += 1
        crop = 0
        print("harvest on day")
        print(day)
print("harvests")
print(harvests)
print(crop)

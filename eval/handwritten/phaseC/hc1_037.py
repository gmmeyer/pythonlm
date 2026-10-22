weight = 40
reps = 12
best = 0
best_set = 0
for s in range(1, 5):
    vol = weight * reps // 10
    print("set " + str(s) + ":", weight, "kg x", reps, "=", vol)
    if vol > best:
        best = vol
        best_set = s
    weight += 5
    reps -= 2
print(f"biggest volume in set {best_set} ({best})")

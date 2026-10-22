boxes = 100
per_pallet = 12
full = 0
while boxes >= per_pallet:
    boxes -= per_pallet
    full += 1
print(full)
print(boxes)
if boxes > 0:
    print("partial pallet needed")

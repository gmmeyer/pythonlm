# A bakery bakes cookies in trays of 18 and sells them in boxes of 12.
# One cookie in every 9 breaks and is eaten by the staff.
# Loose cookies are kept for the next day.

loose = 0
boxes_total = 0
eaten = 0

print("Monday")
trays = 5
baked = trays * 18
broken = baked // 9
eaten += broken
loose += baked - broken
boxes = loose // 12
loose %= 12
boxes_total += boxes
print(boxes)
print(loose)

print("Tuesday")
trays = 7
baked = trays * 18
broken = baked // 9
eaten += broken
loose += baked - broken
boxes = loose // 12
loose %= 12
boxes_total += boxes
print(boxes)
print(loose)

print("Wednesday")
trays = 4
baked = trays * 18
broken = baked // 9
eaten += broken
loose += baked - broken
boxes = loose // 12
loose %= 12
boxes_total += boxes
print(boxes)
print(loose)

print("Thursday")
trays = 9
baked = trays * 18
broken = baked // 9
eaten += broken
loose += baked - broken
boxes = loose // 12
loose %= 12
boxes_total += boxes
print(boxes)
print(loose)

print("--- week ---")
print(boxes_total)
print(eaten)
# a box sells for 7 coins
print(boxes_total * 7)

items = 257
per_box = 12
full = items // per_box
loose = items % per_box
boxes = (items + per_box - 1) // per_box
print(full)
print(loose)
print(boxes)

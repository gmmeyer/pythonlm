local_h = 3
offset = -8
utc_h = (local_h - offset) % 24
print(utc_h)
tokyo = (utc_h + 9) % 24
print(tokyo)

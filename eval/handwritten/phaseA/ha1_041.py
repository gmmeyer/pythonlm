room_w = 36
room_l = 27
tile = 9
cols = room_w // tile
rws = room_l // tile
tiles = cols * rws
print(tiles)
per_box = 5
print(-(-tiles // per_box))

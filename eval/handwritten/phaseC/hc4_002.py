# A box inside a box, built one row at a time from string pieces.
# The outer frame uses '#', the inner frame uses 'o'.
w = 16
h = 9
r = 0
while r < h:
    if r == 0 or r == h - 1:
        line = "#" * w
    elif r == 2 or r == h - 3:
        line = "#  " + "o" * (w - 6) + "  #"
    elif r > 2 and r < h - 3:
        line = "#  o" + " " * (w - 8) + "o  #"
    else:
        line = "#" + " " * (w - 2) + "#"
    print(line, r, sep="  ")
    r += 1
print("outer", w, "x", h, sep=" ")
print("inner", w - 4, "x", h - 4, sep=" ")

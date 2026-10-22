# Parking lot with eight slots shown as a string ('.' free, 'C' taken).
# Cars arrive and leave on a schedule; the string is rebuilt each time.
lot = "........"
used = 0
for t in range(6):
    if t == 0 or t == 1 or t == 3 or t == 4:
        slot = (t * 3) % 8
        ch = "C"
        used += 1
        what = "arrive"
    else:
        slot = ((t - 2) * 3) % 8
        ch = "."
        used -= 1
        what = "leave "
    new = ""
    for k in range(8):
        if k == slot:
            new += ch
        else:
            new += lot[k]
    lot = new
    print(what, slot, "[" + lot + "]", used)
print("free slots:", 8 - used)

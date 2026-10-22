b = "0110"
for step in range(4):
    i = len(b) - 1
    tail = ""
    while i >= 0 and b[i] == "1":
        tail += "0"
        i -= 1
    r = ""
    for k in range(i):
        r += b[k]
    if i < 0:
        r = "1"
    else:
        r += "1"
    b = r + tail
    print(b, end=" ")
print("done")

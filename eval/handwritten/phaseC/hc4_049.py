# A loading spinner: the frame comes from indexing a four-character
# string, the dots cycle, and the percentage climbs to 100.
frames = "|/-\\"
pct = 0
for t in range(12):
    f = frames[t % 4]
    dots = "." * (t % 4)
    pct += 9
    if t == 11:
        pct = 100
    print(f"[{f}] loading{dots}", end="")
    print(" " * (4 - len(dots)) + str(pct) + "%")
print("[*] done", "frames: " + str(len(frames)), sep=" | ")

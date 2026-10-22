name = "bob smith"
bad = 0
for i in range(len(name)):
    c = name[i]
    if c == " " or c == "!" or c == "?":
        bad += 1
        print("bad character at position", i)
if bad == 0:
    print("name ok")
else:
    print(bad, "problem(s) found")

errors = 0
warns = 0
for t in range(1, 8):
    if t % 4 == 0:
        print(f"[{t}] ERROR disk full")
        errors += 1
    elif t % 3 == 0:
        print(f"[{t}] WARN slow reply")
        warns += 1
    else:
        print(f"[{t}] INFO ok")
line = str(errors) + " error"
if errors != 1:
    line += "s"
line += ", " + str(warns) + " warning"
if warns != 1:
    line += "s"
print(line)

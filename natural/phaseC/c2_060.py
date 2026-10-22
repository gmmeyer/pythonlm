raw = "    indented text"
start = 0
while raw[start] == " ":
    start += 1
clean = ""
for i in range(start, len(raw)):
    clean += raw[i]
print("[" + clean + "]", "removed", start, "spaces")

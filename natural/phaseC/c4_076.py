levels = " .:-=+*#"
data = 0
line = ""
for i in range(16):
    data = (data * 5 + 3) % 8
    line += levels[data]
print("|" + line + "|")

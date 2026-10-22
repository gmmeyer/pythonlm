done = 7
total = 10
bar = ""
for i in range(total):
    if i < done:
        bar += "#"
    else:
        bar += "."
print("[" + bar + "]", str(done * 100 // total) + "%")

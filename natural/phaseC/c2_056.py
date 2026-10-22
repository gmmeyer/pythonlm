text = "go to the store and go home"
target = "o"
last = -1
for i in range(len(text) - 1, -1, -1):
    if text[i] == target:
        last = i
        break
print("last", target, "is at index", last)

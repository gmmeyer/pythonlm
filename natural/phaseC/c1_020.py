text = "banana bread"
count = 0
for i in range(len(text)):
    if text[i] == "a":
        count += 1
print(f"{text} has {count} letter a")

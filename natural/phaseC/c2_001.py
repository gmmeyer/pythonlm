text = "a banana and a pineapple"
count = 0
for i in range(len(text)):
    if text[i] == "a":
        count += 1
print("a appears", count, "times in", len(text), "characters")

text = "mississippi"
target = "s"
count = 0
for i in range(len(text)):
    if text[i] == target:
        count += 1
print(f"'{target}' appears {count} times in {text}")

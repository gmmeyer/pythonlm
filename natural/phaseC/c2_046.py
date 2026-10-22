text = "banana bread"
pat = "nan"
found = -1
for i in range(len(text) - len(pat) + 1):
    match = True
    for j in range(len(pat)):
        if text[i + j] != pat[j]:
            match = False
    if match and found == -1:
        found = i
if found == -1:
    print(pat, "not found")
else:
    print(pat, "found at index", found)

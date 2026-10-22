text = "banana"
pat = "ana"
count = 0
for i in range(len(text) - len(pat) + 1):
    match = True
    for j in range(len(pat)):
        if text[i + j] != pat[j]:
            match = False
            break
    if match:
        count += 1
print(f"{pat} occurs {count} times in {text}")

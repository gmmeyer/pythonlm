half = "abc"
full = half
for i in range(len(half) - 1, -1, -1):
    full += half[i]
print(full)

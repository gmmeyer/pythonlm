a = "interview"
b = "internet"
common = ""
i = 0
while i < len(a) and i < len(b) and a[i] == b[i]:
    common += a[i]
    i += 1
print("common prefix:", common)
print("length:", len(common))

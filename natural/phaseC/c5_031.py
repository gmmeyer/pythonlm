s = "aabbabccc"
same_pairs = 0
for i in range(len(s) - 1):
    if s[i] == s[i + 1]:
        same_pairs += 1
print(f"{same_pairs} adjacent equal pairs in {s}")
if same_pairs == 0:
    print("perfectly alternating")

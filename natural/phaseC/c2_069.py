word = "unhappy"
prefix = "un"
is_prefix = len(prefix) <= len(word)
for i in range(len(prefix)):
    if is_prefix and word[i] != prefix[i]:
        is_prefix = False
print(word, "starts with", prefix, ":", is_prefix)

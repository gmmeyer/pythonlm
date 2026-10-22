# Shift cipher over the small alphabet "abcdefgh": each letter moves
# three places forward, wrapping round. Letters are found by scanning.
alpha = "abcdefgh"
word = "badcafe"
out = ""
i = 0
while i < len(word):
    j = 0
    while alpha[j] != word[i]:
        j += 1
    out = out + alpha[(j + 3) % 8]
    i += 1
print(word, "->", out)
print("first", out[0], "last", out[-1])
print("length kept:", len(out) == len(word))

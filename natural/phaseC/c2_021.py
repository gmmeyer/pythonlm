s = "abcdefghij"
evens = ""
odds = ""
for i in range(len(s)):
    if i % 2 == 0:
        evens += s[i]
    else:
        odds += s[i]
print("even positions:", evens)
print("odd positions: ", odds)

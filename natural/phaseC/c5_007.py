# count vowels in either case
s = "Education Is Awesome"
n = 0
for i in range(len(s)):
    c = s[i]
    if (c == "a" or c == "A" or c == "e" or c == "E" or c == "i" or c == "I"
            or c == "o" or c == "O" or c == "u" or c == "U"):
        n += 1
print(s)
print("vowel count:", n)

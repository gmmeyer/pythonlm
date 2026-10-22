s = "abcdefg"
k = 10
n = len(s)
left = ""
right = ""
for i in range(n):
    left += s[(i + k) % n]
    right += s[(i - k) % n]
print(left, right, sep=" / ")

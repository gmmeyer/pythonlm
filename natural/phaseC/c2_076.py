word = "pattern"
n = len(word)
for i in range(n // 2):
    print(word[i] + word[n - 1 - i])
if n % 2 == 1:
    print(word[n // 2])

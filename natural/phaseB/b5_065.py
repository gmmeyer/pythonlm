# Josephus: 7 people in a circle, every 3rd one is out
n = 7
k = 3
safe = 0
for people in range(2, n + 1):
    safe = (safe + k) % people
print(safe + 1)

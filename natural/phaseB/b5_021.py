# climbing stairs one or two at a time: ways to reach step 10
prev = 1
cur = 1
for step in range(2, 11):
    prev, cur = cur, prev + cur
print(cur)

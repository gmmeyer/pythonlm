log = "++-+--++++-"
score = 0
for i in range(len(log)):
    if log[i] == "+":
        score += 1
    else:
        score -= 1
print(f"score after {len(log)} steps: {score}")

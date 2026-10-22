x = "transmission"
y = "transmitting"
n = len(x)
if len(y) < n:
    n = len(y)
i = 0
while i < n and x[i] == y[i]:
    i += 1
if i == n and len(x) == len(y):
    print("same")
else:
    print(f"differ at {i}: {x[i]} vs {y[i]}")

x = "12345"
y = "abc"
out = ""
n = len(x)
if len(y) > n:
    n = len(y)
for i in range(n):
    if i < len(x):
        out += x[i]
    if i < len(y):
        out += y[i]
print(f"merged: {out}")

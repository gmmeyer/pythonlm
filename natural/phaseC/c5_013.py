x = "level"
y = "lever"
same = True
if len(x) != len(y):
    same = False
else:
    for i in range(len(x)):
        if x[i] != y[i]:
            same = False
print("my check:", same)
print("built-in agrees:", same == (x == y))

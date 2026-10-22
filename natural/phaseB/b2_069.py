# robot returns home: walks right then back left
pos = 0
for i in range(5):
    pos += 3
print(pos)
for i in range(5):
    pos -= 3
print(pos)
print(pos == 0)

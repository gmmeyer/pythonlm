# seeded LCG coin flips: heads when the state is even
x = 7
heads = 0
for flip in range(1, 21):
    x = (x * 5 + 3) % 16
    if x % 2 == 0:
        heads += 1
print(heads)
print(20 - heads)

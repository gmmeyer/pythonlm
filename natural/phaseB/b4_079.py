# first square above 200
i = 1
while i * i <= 200:
    i += 1
if i * i > 200:
    print(i)
    print(i * i)
else:
    print(0)

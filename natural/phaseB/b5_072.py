# reverse the 8 bits of 22 (00010110 becomes 01101000)
n = 22
rev = 0
for i in range(8):
    rev = rev * 2 + n % 2
    n //= 2
print(rev)

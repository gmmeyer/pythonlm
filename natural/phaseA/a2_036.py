# 99 always divides n minus its reverse
n = 825
rev = n % 10 * 100 + n // 10 % 10 * 10 + n // 100
diff = n - rev
print(diff)
print(diff // 99)
print(diff % 99)

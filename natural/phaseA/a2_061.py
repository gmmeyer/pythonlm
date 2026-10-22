# 12 hour clock where the hand points at 12, not 0
hour = 7
print((hour + 30 - 1) % 12 + 1)
hour = 11
print((hour + 100 - 1) % 12 + 1)

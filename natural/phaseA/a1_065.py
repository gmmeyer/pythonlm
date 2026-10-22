# 11:30 pm to 1:15 am, counting on a 12 hour clock
night = 11 * 60 + 30
morning = 1 * 60 + 15
diff = morning - night
print(diff)
print(diff % 60)
print(diff // 60)
print(diff + 12 * 60)

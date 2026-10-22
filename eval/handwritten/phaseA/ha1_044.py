# plates per side for a 185 lb bar
target = 185
bar = 45
each_side = (target - bar) // 2
p45 = each_side // 45
rest = each_side % 45
p10 = rest // 10
p5 = rest % 10 // 5
print("45s")
print(p45)
print("10s")
print(p10)
print("5s")
print(p5)

# A kitchen timer is set to 10 minutes (600 seconds) for a stew.
# We check it at a few moments and show the time left as minutes
# and seconds. In the end the stew is left too long.

timer = 600
elapsed = 0

print("Set")
print(timer // 60)
print(timer % 60)

print("Stir after 2:05")
elapsed += 125
left = timer - elapsed
print(left // 60)
print(left % 60)

print("Carrots in at 4:50")
elapsed = 4 * 60 + 50
left = timer - elapsed
print(left // 60)
print(left % 60)

print("Needs longer: add 2:30")
timer += 150
left = timer - elapsed
print(left // 60)
print(left % 60)

print("Phone call: 3:47 passes")
elapsed += 227
left = timer - elapsed
print(left // 60)
print(left % 60)

print("Forgot it! 40 s too long")
elapsed = timer + 40
left = timer - elapsed
print(left)
# floor division of a negative time rounds down
print(left // 60)
print(left % 60)
print(-left // 60)
print(-left % 60)

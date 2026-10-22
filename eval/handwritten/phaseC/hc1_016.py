first = "maria"
last = "lopez"
yy = 94
user = first[0] + last + str(yy)
print("suggested username:", user)
alt = last[0] + "_" + first + str(yy + 1)
print("or maybe:", alt)
if len(user) > 6:
    print("(that is", len(user), "characters, a bit long)")
else:
    print("nice and short")

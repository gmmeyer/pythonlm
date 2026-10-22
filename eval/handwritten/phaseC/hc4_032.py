# Plot of y = (x - 6) * (x - 6) // 4 sideways: one row per x value,
# with the point drawn after y spaces and the axis on the left.
for x in range(13):
    y = (x - 6) * (x - 6) // 4
    if y == 0:
        mark = "o<- min"
    else:
        mark = "o"
    print(str(x) + " " * (3 - len(str(x))) + "|" + " " * y + mark)
print("   +" + "-" * 10)

results = "WWLWWWLLWW"
streak = 0
longest = 0
i = 0
while i < len(results):
    if results[i] == "W":
        streak = streak + 1
    else:
        streak = 0
    if streak > longest:
        longest = streak
    i = i + 1
print("games:", len(results))
print("best winning streak:", longest)

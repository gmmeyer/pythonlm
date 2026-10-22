awake = 0
for hour in range(2, 24, 4):
    if hour < 5 or hour >= 22:
        print("go back to sleep")
        continue
    awake += 1
    if hour < 12:
        print("good morning")
    elif hour < 17:
        print("good afternoon")
    else:
        print("good evening")
print(awake)

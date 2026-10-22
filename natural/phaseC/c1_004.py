# progress bar built one step at a time
done = ""
for step in range(1, 11):
    done = done + "#"
    left = " " * (10 - step)
    print("[" + done + left + "]", step * 10, "%")

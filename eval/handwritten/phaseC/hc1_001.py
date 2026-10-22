tasks_total = 6
status = ""
done = 0
for t in range(tasks_total):
    if t % 3 == 2:
        status += "[ ]"
    else:
        status += "[x]"
        done += 1
print("todo:", status)
left = tasks_total - done
print(f"{done}/{tasks_total} done, {left} left")
if left == 0:
    print("all clear")
elif left == 1:
    print("one more thing")
else:
    print("still " + str(left) + " to go")

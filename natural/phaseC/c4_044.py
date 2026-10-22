total = 4
done = 0
for task in range(1, total + 1):
    if task % 2 == 1:
        done += 1
        status = "done"
    else:
        status = "open"
    print(f"task {task}: {status}")
left = total - done
word = "tasks"
if left == 1:
    word = "task"
print(f"{done} of {total} done, {left} {word} left")

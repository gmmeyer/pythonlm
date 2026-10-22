# word ladder with step numbers; only report real changes
word = "lead"
goal = "gold"
step = 0
print("start:", word)
for pos in range(len(word)):
    if word[pos] != goal[pos]:
        new = ""
        for i in range(len(word)):
            if i == pos:
                new += goal[pos]
            else:
                new += word[i]
        word = new
        step += 1
        print(f"step {step}: {word}")
print("reached", goal, "in", step, "steps")

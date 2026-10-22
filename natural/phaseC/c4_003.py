# coin-operated turnstile
state = "locked"
for step in range(1, 9):
    if step % 3 == 0:
        action = "push"
    else:
        action = "coin"
    if state == "locked" and action == "coin":
        state = "open"
    elif state == "open" and action == "push":
        state = "locked"
    print(f"{step}: {action} -> {state}")

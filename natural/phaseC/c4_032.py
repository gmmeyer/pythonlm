state = "idle"
coins = 0
for event in range(1, 10):
    if state == "idle" and event % 2 == 1:
        state = "paid"
        coins += 1
    elif state == "paid" and event % 3 == 0:
        state = "dispensing"
    elif state == "dispensing":
        state = "idle"
    print("event", event, "state", state)
print("coins taken:", coins)

secret = "open"
attempt = "close"
tries = 0
locked = False
while attempt != secret and not locked:
    tries += 1
    print("attempt", tries, "-", attempt, "denied")
    if tries == 2:
        attempt = "shut"
    elif tries == 3:
        attempt = "open"
    elif tries >= 5:
        locked = True
if locked:
    print("account locked")
else:
    print("welcome after", tries, "failures")

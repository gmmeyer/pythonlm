# retry with doubling delay, capped at 40
delay = 1
waited = 0
tries = 0
success_on = 4
while tries < 6:
    tries += 1
    if tries == success_on:
        print("connected")
        break
    waited += delay
    delay = delay * 2
    if delay > 40:
        delay = 40
print(tries)
print(waited)

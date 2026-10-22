# thermostat: stop once the room has reached 20 or ten steps have passed
temp = 5
steps = 0
while True:
    steps += 1
    temp += 2
    if temp >= 20:
        print("warm")
        break
    if steps == 10:
        print("timeout")
        break
print(temp)

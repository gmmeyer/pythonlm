# A clock that jumps 25 minutes per tick, carrying minutes into hours and
# wrapping hour 24 back to 0. An alarm rings once the hour reaches 7.
hour = 23
minute = 10
days = 0
alarm_done = True
print("clock running")
for tick in range(19):
    minute += 25
    if minute >= 60:
        minute -= 60
        hour += 1
        if hour == 24:
            hour = 0
            days += 1
            alarm_done = False
            print("midnight")
        print(hour)
    if hour >= 7 and not alarm_done:
        alarm_done = True
        print("alarm rings")
print("days passed")
print(days)
print(hour)
print(minute)

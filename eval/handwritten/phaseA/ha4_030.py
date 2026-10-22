# Days of the week are numbered 0 (Monday) to 6 (Sunday).
# Today is a Wednesday (2). We work out the weekday of a few events,
# going forward and backward in time; % 7 handles both directions.

today = 2

print("Dentist in 10 days")
day = (today + 10) % 7
print(day)

print("Concert in 45 days")
concert = today + 45
print(concert % 7)

print("Deadline 3 weeks 4 days later")
deadline = concert + 3 * 7 + 4
print(deadline % 7)
print(deadline - today)

print("Birthday 100 days ago")
day = (today - 100) % 7
print(day)

print("Holiday in 365 days")
span = 365
day = (today + span) % 7
print(day)
print(span // 7)
print(span % 7)

print("Moon festival every 29 days")
fest = today
fest = (fest + 29) % 7
print(fest)
fest = (fest + 29) % 7
print(fest)
fest = (fest + 29) % 7
print(fest)

print("Back 6 weeks and 2 days")
day = (today - 6 * 7 - 2) % 7
print(day)
print(-6 * 7 - 2)

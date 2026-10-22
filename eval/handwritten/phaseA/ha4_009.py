# A local train stops at six stations. At each stop some of the people
# aboard get off and new ones get on. Every boarding ticket costs 3 coins.

aboard = 0
tickets_sold = 0
capacity = 120

print("Station: Harbor")
boarding = 46
aboard += boarding
tickets_sold += boarding
print(aboard)

print("Station: Market")
leaving = aboard // 4
boarding = 31
aboard += boarding - leaving
tickets_sold += boarding
print(aboard)

print("Station: University")
leaving = aboard // 2
boarding = 58
aboard += boarding - leaving
tickets_sold += boarding
print(aboard)
print(capacity - aboard)

print("Station: Hospital")
leaving = aboard // 3 + 4
boarding = 17
aboard += boarding - leaving
tickets_sold += boarding
print(aboard)

print("Station: Park")
leaving = aboard * 3 // 5
boarding = 9
aboard += boarding - leaving
tickets_sold += boarding
print(aboard)

print("Station: Terminus")
leaving = aboard
aboard -= leaving
print(leaving)
print(aboard)

print("--- summary ---")
print(tickets_sold)
print(tickets_sold * 3)

# An elevator in a 12-floor building, moved call by call.
# A trip is (target - current). Going down the trip is negative,
# so we subtract it from the distance to keep the distance positive.

current_floor = 1
floors_travelled = 0
passengers = 0
weight_per_person = 75

print("Call from floor 7")
trip = 7 - current_floor
floors_travelled += trip
current_floor += trip
passengers += 3
print(current_floor)
print(passengers * weight_per_person)

print("Ride down to floor 2")
trip = 2 - current_floor
floors_travelled -= trip
current_floor += trip
passengers -= 2
print(current_floor)
print(trip)

print("Call from floor 11")
trip = 11 - current_floor
floors_travelled += trip
current_floor += trip
passengers += 5
print(current_floor)
print(passengers * weight_per_person)

print("Express down to the basement (floor -1)")
trip = -1 - current_floor
floors_travelled -= trip
current_floor += trip
passengers = 0
print(current_floor)
print(trip)

print("Maintenance check: up to floor 9 and back down")
trip = 9 - current_floor
floors_travelled += trip
floors_travelled += trip
print(trip)

print("--- summary ---")
print(floors_travelled)
# the elevator needs 3 seconds per floor
print(floors_travelled * 3)
print(floors_travelled * 3 // 60)
print(floors_travelled * 3 % 60)

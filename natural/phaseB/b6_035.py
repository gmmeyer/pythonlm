# taxi fare: base 5, 2 per km after the first 3, night surcharge of 20 percent
km = 11
night = True
fare = 5
if km > 3:
    fare += (km - 3) * 2
if night:
    fare += fare * 20 // 100
print(fare)

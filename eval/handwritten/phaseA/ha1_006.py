# road trip: three legs
leg1 = 180
leg2 = 245
leg3 = 130
total_km = leg1 + leg2 + leg3
print("total km")
print(total_km)

# car does about 7 litres per 100 km
use = 7
fuel = total_km // 10 * use // 10
print("litres")
print(fuel)

tank = 50
in_tank = 20
need = fuel - in_tank
stops = (need + tank - 1) // tank
print("fuel stops")
print(stops)

# average 80 km/h, and 60/80 is 3/4
speed = 80
hrs = total_km // speed
mins = total_km % speed * 3 // 4
print(hrs)
print(mins)

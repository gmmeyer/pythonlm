# end of season table, 3 teams
# 3 points for a win, 1 for a draw
rovers_w = 14
rovers_d = 9
rovers_l = 7
rovers_gf = 41
rovers_ga = 33

city_w = 15
city_d = 5
city_l = 10
city_gf = 47
city_ga = 39

united_w = 9
united_d = 12
united_l = 9
united_gf = 30
united_ga = 35

rovers = rovers_w * 3 + rovers_d
city = city_w * 3 + city_d
united = united_w * 3 + united_d

print("Rovers")
print(rovers)
print(rovers_gf - rovers_ga)
print("City")
print(city)
print(city_gf - city_ga)
print("United")
print(united)
print(united_gf - united_ga)

# gap at the top, and how far back United is
print(rovers - city)
print(united - rovers)

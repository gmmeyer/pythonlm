# a train leaves at 9:45 and arrives at 14:20
depart = 9 * 60 + 45
arrive = 14 * 60 + 20
trip = arrive - depart
print(trip // 60)
print(trip % 60)

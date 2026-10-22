# cabin weekend, 5 people
hotel = 360
gas = 84
food = 150
deposit_back = -45
total = hotel + gas + food + deposit_back
n = 5
share = total // n
print("each pays")
print(share)
print("organizer covers")
print(total - share * n)

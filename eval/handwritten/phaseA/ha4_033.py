# A hotel with 60 rooms over a long weekend.
# A room costs 9 (in tens of coins) a night, only 6 on Sunday.
# Revenue is kept as hundreds plus the rest, so the numbers stay small.

rooms = 60
booked = 0
rev_hundreds = 0
rev_rest = 0
rate = 9

print("Thursday")
booked += 22
rev_rest += booked * rate
rev_hundreds += rev_rest // 100
rev_rest %= 100
print(booked)
print(rooms - booked)

print("Friday")
# 31 arrive, 5 leave
booked += 31 - 5
rev_rest += booked * rate
rev_hundreds += rev_rest // 100
rev_rest %= 100
print(booked)
print(rooms - booked)

print("Saturday: full house")
booked += 12
rev_rest += booked * rate
rev_hundreds += rev_rest // 100
rev_rest %= 100
print(booked)
print(rooms - booked)

print("Sunday: cheap night")
rate = 6
booked -= 35
rev_rest += booked * rate
rev_hundreds += rev_rest // 100
rev_rest %= 100
print(booked)
# occupancy in tenths
print(booked * 10 // rooms)

print("--- weekend ---")
print(rev_hundreds)
print(rev_rest)

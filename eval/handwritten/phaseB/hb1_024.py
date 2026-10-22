# library late fees, in cents, capped at five dollars
fee_per_day = 25
cap = 500
for days_late in range(0, 31, 6):
    fee = days_late * fee_per_day
    if fee > cap:
        fee = cap
    if days_late == 0:
        print("returned on time")
    else:
        print(fee)

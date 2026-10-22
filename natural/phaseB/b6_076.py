# raffle: tickets divisible by 7 or 11 win a prize, find the first winner after 40
ticket = 40
found = False
while found == False:
    ticket = ticket + 1
    if ticket % 7 == 0 or ticket % 11 == 0:
        found = True
print(ticket)

winner = 0
for ticket in range(100, 121):
    if ticket % 7 == 0:
        winner = ticket
        print(f"Ticket {ticket} wins a prize!")
if winner == 0:
    print("No winner")
else:
    print("Last winner:", winner)

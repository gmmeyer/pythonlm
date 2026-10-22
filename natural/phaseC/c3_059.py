for n in range(7, 130, 40):
    num = str(n)
    ticket = "0" * (4 - len(num)) + num
    print("Ticket no.", ticket)

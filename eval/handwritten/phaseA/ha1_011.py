# overdrawn card paid off in 6 installments
balance = -47
installments = 6
per = balance // installments
rest = balance % installments
print(per)
print(rest)
print(per * installments + rest)

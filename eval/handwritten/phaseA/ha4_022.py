# A village library with 250 books, followed for one week.
# Late books are fined 2 coins for every day they are late.

shelf = 250
on_loan = 0
fines = 0

print("Monday")
borrowed = 34
shelf -= borrowed
on_loan += borrowed
print(shelf)

print("Tuesday")
borrowed = 21
returned = 12
shelf += returned - borrowed
on_loan += borrowed - returned
print(shelf)

print("Wednesday")
returned = 18
# three of them came back 4 days late
late = 3
days_late = 4
fines += late * days_late * 2
shelf += returned
on_loan -= returned
print(shelf)
print(fines)

print("Thursday: donation")
shelf += 40
borrowed = 27
shelf -= borrowed
on_loan += borrowed
print(shelf)

print("Friday")
returned = 30
late = 5
days_late = 2
fines += late * days_late * 2
shelf += returned
on_loan -= returned
print(shelf)
print(fines)

print("Saturday: busy")
# one book in ten on the shelf goes out
borrowed = shelf // 10
shelf -= borrowed
on_loan += borrowed
print(borrowed)
print(shelf)

print("Sunday: closed")
print()

print("--- week ---")
print(shelf + on_loan)
print(on_loan)
print(fines)

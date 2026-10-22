# A tiny library has 5 copies of a popular book. Loans come back after
# four days, tracked by four counters that shift down each day like a
# conveyor. Readers who find no copy join a waiting list.
copies = 5
d1 = 0
d2 = 0
d3 = 0
d4 = 0
waitlist = 0
print("library desk")
for day in range(13):
    copies += d4
    d4 = d3
    d3 = d2
    d2 = d1
    want = (day % 4 + 2) // 2 + waitlist
    got = want
    if got > copies:
        got = copies
    waitlist = want - got
    copies -= got
    d1 = got
    print(copies)
    if waitlist > 0:
        print("readers waiting")
        print(waitlist)
print("waiting list")
print(waitlist)
print(copies + d1 + d2 + d3 + d4 == 5)

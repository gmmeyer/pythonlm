# A 4 x 100 m relay. Leg times are in tenths of a second.
# The first leg loses 7 tenths at the start and every hand-over loses 2.
# Between heats the coach reorders the runners with tuple swaps.

bib1 = 11
bib2 = 27
bib3 = 34
bib4 = 46
leg1 = 118
leg2 = 121
leg3 = 119
leg4 = 112

print("Heat 1")
total = leg1 + 7 + leg2 + 2 + leg3 + 2 + leg4 + 2
print(total // 10)
print(total % 10)

print("Heat 2: first and last swap")
bib1, bib4 = bib4, bib1
leg1, leg4 = leg4, leg1
# everyone is warmed up now: one tenth faster
leg1 -= 1
leg2 -= 1
leg3 -= 1
leg4 -= 1
total = leg1 + 7 + leg2 + 2 + leg3 + 2 + leg4 + 2
print(bib1)
print(bib4)
print(total // 10)
print(total % 10)

print("Heat 3: middle three rotate")
bib2, bib3, bib4 = bib3, bib4, bib2
leg2, leg3, leg4 = leg3, leg4, leg2
# the new starter practiced his start
leg1 -= 2
total = leg1 + 7 + leg2 + 2 + leg3 + 2 + leg4 + 2
print(total // 10)
print(total % 10)

print("--- final order ---")
print(bib1)
print(bib2)
print(bib3)
print(bib4)

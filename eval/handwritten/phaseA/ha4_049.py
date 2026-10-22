# Two planets circle a star; angles are in degrees from 0 to 359.
# The inner planet moves 47 degrees a month, the outer one 13,
# and a comet goes the other way at 29 degrees a month.

inner = 0
outer = 90
comet = 150

print("Month 1")
inner = (inner + 47) % 360
outer = (outer + 13) % 360
comet = (comet - 29) % 360
print((inner - outer) % 360)

print("Month 2")
inner = (inner + 47) % 360
outer = (outer + 13) % 360
comet = (comet - 29) % 360
print((inner - outer) % 360)

print("Month 3")
inner = (inner + 47) % 360
outer = (outer + 13) % 360
comet = (comet - 29) % 360
print((inner - outer) % 360)

print("Month 4")
inner = (inner + 47) % 360
outer = (outer + 13) % 360
comet = (comet - 29) % 360
print((inner - outer) % 360)

print("Month 5")
inner = (inner + 47) % 360
outer = (outer + 13) % 360
comet = (comet - 29) % 360
print((inner - outer) % 360)

print("Month 6")
inner = (inner + 47) % 360
outer = (outer + 13) % 360
comet = (comet - 29) % 360
print((inner - outer) % 360)

print("--- positions ---")
print(inner)
print(outer)
print(comet)
print((comet - inner) % 360)

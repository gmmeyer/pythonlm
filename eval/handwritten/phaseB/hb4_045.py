# A mouse runs down a corridor toward cheese at cell 15. Doors stand in
# front of cells 6 and 12 and are open only on even ticks, so on odd ticks
# the mouse waits. Every seventh tick a cat scares it back two cells.
cell = 0
tick = 0
waits = 0
scares = 0
print("mouse in the corridor")
while cell < 15:
    tick += 1
    if tick % 7 == 0:
        cell -= 2
        scares += 1
        print("cat")
        print(cell)
        continue
    if (cell + 1) % 6 == 0 and tick % 2 == 1:
        waits += 1
        continue
    cell += 1
print("cheese reached at tick")
print(tick)
print(waits)
print(scares)

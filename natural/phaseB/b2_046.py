# population with births and deaths, stops at a limit or extinction
pop = 30
gen = 0
while 0 < pop < 120:
    gen += 1
    births = pop // 3
    deaths = 4 + gen
    pop = pop + births - deaths
print(gen)
print(pop)

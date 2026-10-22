# printer: 20 pages a minute, ink for 150 pages
ink = 150
pages_done = 0
minutes = 0
job = 220
while pages_done < job:
    if ink < 20:
        print("out of ink")
        break
    pages_done += 20
    ink -= 20
    minutes += 1
print(pages_done)
print(minutes)

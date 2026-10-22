# bus runs every 12 minutes starting at minute 5; how many in the first hour?
k = 12
t = 5
arrivals = 0
while t <= 60:
    arrivals += 1
    t += k
print(arrivals)
print(t)

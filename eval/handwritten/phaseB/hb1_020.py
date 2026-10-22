# climb two stairs at a time, catch your breath every 10
step = 0
rests = 0
top = 37
while step < top:
    if top - step == 1:
        step += 1
    else:
        step += 2
    if step % 10 == 0:
        rests += 1
print(step)
print(rests)

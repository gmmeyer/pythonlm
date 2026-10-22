# ping pong game: say Ping on evens, Pong on multiples of 3
for k in range(1, 19):
    msg = ""
    if k % 2 == 0:
        msg = "Ping"
    if k % 3 == 0:
        msg = msg + "Pong"
    if msg != "":
        print(k, msg)

for i in range(1, 19):
    if i % 6 == 0:
        print("PingPong")
    elif i % 2 == 0:
        print("Ping")
    elif i % 3 == 0:
        print("Pong")
    else:
        print(i)

m = 10
K = 26
J = 20
for q in range(22, 25):
    h = (q + 13 * (m + 1) // 5 + K + K // 4 + J // 4 + 5 * J) % 7
    if h == 0:
        print('Sat')
    elif h == 1:
        print('Sun')
    elif h == 2:
        print('Mon')
    elif h == 3:
        print('Tue')
    elif h == 4:
        print('Wed')
    elif h == 5:
        print('Thu')
    else:
        print('Fri')

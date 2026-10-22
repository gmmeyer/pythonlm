A = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
n = 25
while n < 700:
    m = n
    lab = ""
    while m > 0:
        m -= 1
        lab = A[m % 26] + lab
        m //= 26
    print(n, lab, sep=" -> ")
    n += 300

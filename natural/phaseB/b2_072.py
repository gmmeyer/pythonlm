# hot or cold game with a pseudo-random secret
x = 11
secret = (x * 7 + 3) % 101
guess = 50
tries = 0
while guess != secret and tries < 20:
    if guess < secret:
        guess += 7
    else:
        guess -= 5
    tries += 1
print(secret)
print(guess)
print(tries)

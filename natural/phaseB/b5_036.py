# the service never recovers, so we give up after 4 tries
max_tries = 4
tries = 0
healthy = False
while not healthy and tries < max_tries:
    tries += 1
    healthy = tries > 9
if healthy:
    print("ok")
else:
    print("gave up")
print(tries)

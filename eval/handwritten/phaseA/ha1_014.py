# shift swap at the cafe
alice_shift = 6
bob_shift = 9
alice_rate = 15
bob_rate = 13
print(alice_shift * alice_rate)
print(bob_shift * bob_rate)
alice_shift, bob_shift = bob_shift, alice_shift
print("after swap")
print(alice_shift * alice_rate)
print(bob_shift * bob_rate)

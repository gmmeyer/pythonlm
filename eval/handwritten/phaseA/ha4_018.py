# Ada and Ben play four hands of a card game. A hand is worth the
# last digit of the sum of its two cards, and the dealer gets a bonus.
# After each hand the roles switch, so the two totals are swapped.
# Ada deals first; after an even number of swaps she deals again.

dealer = 0
player = 0
bonus = 2

print("Hand 1: Ada deals")
card1 = 7
card2 = 9
dealer += (card1 + card2) % 10 + bonus
card1 = 8
card2 = 8
player += (card1 + card2) % 10
print(dealer)
print(player)
dealer, player = player, dealer

print("Hand 2: Ben deals")
card1 = 3
card2 = 4
dealer += (card1 + card2) % 10 + bonus
card1 = 9
card2 = 1
player += (card1 + card2) % 10
print(dealer)
print(player)
dealer, player = player, dealer

print("Hand 3: Ada deals")
card1 = 5
card2 = 5
dealer += (card1 + card2) % 10 + bonus
card1 = 6
card2 = 7
player += (card1 + card2) % 10
print(dealer)
print(player)
dealer, player = player, dealer

print("Hand 4: Ben deals")
card1 = 9
card2 = 9
dealer += (card1 + card2) % 10 + bonus
card1 = 4
card2 = 5
player += (card1 + card2) % 10
print(dealer)
print(player)
dealer, player = player, dealer

print("--- final ---")
print("Ada")
print(dealer)
print("Ben")
print(player)
print(player - dealer)

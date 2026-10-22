# A fish pond. Each year the stock grows by a fifth plus 2 hatchlings,
# capped at 300. A drought every fourth year halves it. The fishing quota
# is a fifth of the stock when there are over 100 fish, otherwise just 5.
fish = 60
caught = 0
print("fish pond")
for year in range(1, 15):
    fish += fish // 5 + 2
    if fish > 300:
        fish = 300
    if year % 4 == 0:
        fish //= 2
        print("drought")
    if fish > 100:
        catch = fish // 5
    else:
        catch = 5
    if catch > fish:
        catch = fish
    fish -= catch
    caught += catch
    print(fish)
print("total caught")
print(caught)

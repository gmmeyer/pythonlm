# A blitz chess game. Each player starts with 300 seconds and gets
# 3 extra seconds for every move. Clocks are shown as minutes, seconds.

white = black = 300
increment = 3

print("Moves 1-10")
white -= 41
black -= 55
white += increment * 10
black += increment * 10
print(white // 60)
print(white % 60)
print(black // 60)
print(black % 60)

print("Moves 11-20")
white -= 97
black -= 62
white += increment * 10
black += increment * 10
print(white // 60)
print(white % 60)
print(black // 60)
print(black % 60)

print("Moves 21-30")
white -= 140
black -= 88
white += increment * 10
black += increment * 10
print(white // 60)
print(white % 60)
print(black // 60)
print(black % 60)

print("Moves 31-35")
white -= 80
black -= 150
white += increment * 5
black += increment * 5
print(white // 60)
print(white % 60)
print(black // 60)
print(black % 60)

print("--- who is ahead ---")
print(white - black)
print(black - white)

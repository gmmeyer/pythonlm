hour = 19
title = "Space Cats"
if hour < 12:
    show = "matinee"
    cost = 6
elif hour < 18:
    show = "afternoon"
    cost = 8
else:
    show = "evening"
    cost = 11
print(f"Ticket for {title} at {hour}h ({show} show)")
print(f"Cost: {cost}")

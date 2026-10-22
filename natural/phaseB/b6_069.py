price = 120
coupon_a = 15
coupon_b = price * 10 // 100
if coupon_a > coupon_b:
    best = coupon_a
else:
    best = coupon_b
print(price - best)
print(coupon_a > coupon_b)

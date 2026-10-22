widget = 35
gadget = 120
n_w = 4
n_g = 2
subtotal = widget * n_w + gadget * n_g
print(f"widgets: {n_w} x {widget}")
print(f"gadgets: {n_g} x {gadget}")
print(f"subtotal: {subtotal}")
if subtotal >= 300:
    off = subtotal // 10
    print(f"10% off: -{off}")
else:
    off = 0
    print("no discount this time")
print("pay", subtotal - off, sep=": ")

# postage is 2 per 100 g but never more than 15
weight = 480
postage = weight // 100 * 2 + 2
if postage > 15:
    postage = 15
print(postage)

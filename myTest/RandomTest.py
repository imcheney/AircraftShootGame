#测试随机数种子的问题

import random

random.seed(10)
print(random.randint(15, 20))
random.seed(10)
print(random.randint(15, 20))
random.seed(10)
print(random.randint(15, 20))
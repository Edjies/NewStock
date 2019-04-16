# -*- coding:utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
### 1 figure

fig = plt.figure()
fig.suptitle('abc')
(a1, a2, a3), (a4, a5, a6) = fig.subplots(2, 3)
x = np.arange(0, 10, 0.2)
a1.plot(x, np.sin(x), marker='x')
a1.axis([-15, 15, -1, 1]) # 指定x轴范围
a2.plot(x, np.cos(x))


a3.plot(x, np.tan(x))
a4.plot(x, x**2)
plt.show()




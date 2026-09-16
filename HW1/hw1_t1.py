'''
Author: NaoMenDDD 2017954808@qq.com
Date: 2026-09-14 19:44:26
LastEditors: NaoMenDDD 2017954808@qq.com
LastEditTime: 2026-09-14 19:59:25
Description: 绘制简谐振动的轨迹
'''
import numpy as np
import matplotlib.pyplot as plt

# 1. 设定时间参数，尽量使曲线平滑
t = np.linspace(0, 2*np.pi, 10000)

# 2. x 和 y 的位移
x = 3 * np.sin(3 * t)
y = 3 * np.sin(3 * t + np.pi/6)

# 3. 绘制轨迹
plt.figure(figsize=(6, 6))
plt.plot(x, y, label=f'Phase Diff = {np.pi/6:.2f} rad (30°)', color='blue')

# 设置坐标轴和图例
plt.title('Vibration Trajectory (x-y Plane)')
plt.xlabel('x')
plt.ylabel('y')
plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
plt.axvline(0, color='black', linewidth=0.8, linestyle='--')
plt.legend()
plt.grid(True)
plt.axis('equal')
plt.show()
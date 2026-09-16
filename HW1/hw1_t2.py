'''
Author: NaoMenDDD 2017954808@qq.com
Date: 2026-09-14 19:54:31
LastEditors: NaoMenDDD 2017954808@qq.com
LastEditTime: 2026-09-15 23:40:12
Description: 绘制简谐振动的轨迹，分析参数变化对轨迹的影响
'''
import numpy as np
import matplotlib.pyplot as plt

# 设定时间参数
t = np.linspace(0, 2*np.pi, 10000)

# 1：改变相位差 (固定频率, 固定振幅)
fig1, axs1 = plt.subplots(1, 3, figsize=(15, 4))
fig1.suptitle('Varying Phase Difference (Fixed Frequency ω=3, Amplitude A=3)', fontsize=16)

phases = [0, np.pi/6, np.pi/2]
titles_phase = ['Δφ = 0 (Straight Line)', 'Δφ = π/6 (Oblique Ellipse)', 'Δφ = π/2 (Circle)']

for i, ax in enumerate(axs1):
    x = 3 * np.sin(3 * t)
    y = 3 * np.sin(3 * t + phases[i])
    ax.plot(x, y, color='blue')
    ax.set_title(titles_phase[i], fontsize=12)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.axis('equal') 
    ax.grid(True)

plt.tight_layout()


# 2：改变频率比 (固定相位差=0, 固定振幅) 
fig2, axs2 = plt.subplots(1, 3, figsize=(15, 4))
fig2.suptitle('Varying Frequency Ratio (Fixed Phase Difference Δφ=0, Amplitude A=3)', fontsize=16)

omegas = [(3, 3), (3, 4), (3, 6)] # 频率比分别为 1:1, 3:4, 1:2
titles_freq = ['ωx=3, ωy=3 (1:1)', 'ωx=3, ωy=4 (3:4)', 'ωx=3, ωy=6 (1:2)']

for i, ax in enumerate(axs2):
    wx, wy = omegas[i]
    x = 3 * np.sin(wx * t)
    y = 3 * np.sin(wy * t) # 相位差设为0
    ax.plot(x, y, color='green')
    ax.set_title(titles_freq[i], fontsize=12)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.axis('equal')
    ax.grid(True)

plt.tight_layout()


# 3：改变振幅 (固定频率比=1:1, 固定相位差=π/6) 
fig3, axs3 = plt.subplots(1, 3, figsize=(15, 4))
fig3.suptitle('Varying Amplitude (Fixed Frequency Ratio 1:1, Phase Difference Δφ=π/6)', fontsize=16)

amplitudes = [(3, 3), (3, 1), (1, 3)] # (Ax, Ay) 的数值
titles_amp = ['Ax=3, Ay=3 (Original)', 'Ax=3, Ay=1 (Compress Y)', 'Ax=1, Ay=3 (Compress X)']

for i, ax in enumerate(axs3):
    Ax, Ay = amplitudes[i]
    x = Ax * np.sin(3 * t)
    y = Ay * np.sin(3 * t + np.pi/6) # 相位差设为 π/6
    ax.plot(x, y, color='red')
    ax.set_title(titles_amp[i], fontsize=12)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.axis('equal')
    ax.grid(True)

plt.tight_layout()

plt.show()
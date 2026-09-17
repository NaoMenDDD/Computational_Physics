# -*- coding: utf-8 -*-
"""
计算物理 第二次作业：alpha 粒子探测器的能量标定

题目：已知若干标准 alpha 源的能量 E 及其对应的信号幅度 S（见 data_HW.txt），
      求信号幅度为 S0 = 1502 mV 的未知粒子的能量。

方法（三种，互相校核）：
  1) 正向拟合   S = a*E + b      （E 为自变量），反解 E0 = (S0 - b) / a
  2) 反向拟合   E = p*S + q      （S 为自变量），直接给出 E0 = p*S0 + q
  3) 线性插值   取 S0 相邻的两点做线性插值

输出：终端打印全部结果，并保存两张图到 imgs/
"""

import numpy as np
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

DATA_FILE = 'data_HW.txt'
S0 = 1502.0            # 待测粒子的信号幅度 (mV)


def load_data(path):
    """从数据文件读取 E 和 S。文件两行，制表符分隔，每行首个字段为标签。"""
    with open(path, encoding='utf-8') as f:
        lines = [ln.strip() for ln in f if ln.strip()]
    # 首字段是名称标签，其余为数据
    E = np.array([float(v) for v in lines[0].split('\t')[1:]], dtype=float)
    S = np.array([float(v) for v in lines[1].split('\t')[1:]], dtype=float)
    return E, S


E, S = load_data(DATA_FILE)
n = len(E)
Ebar, Sbar = E.mean(), S.mean()
Sxx = np.sum((E - Ebar) ** 2)      # E 的离差平方和
Sss = np.sum((S - Sbar) ** 2)      # S 的离差平方和

print('=' * 62)
print('标定数据 (n = %d)' % n)
print('-' * 62)
print('  E (keV): ' + ''.join('%8d' % v for v in E))
print('  S (mV) : ' + ''.join('%8d' % v for v in S))
print('=' * 62)

# ----------------------------------------------------------------------
# 1. 正向拟合 S = a*E + b，反解 E0
# ----------------------------------------------------------------------
a, b = np.polyfit(E, S, 1)
S_fit = a * E + b
resid = S - S_fit
dof = n - 2
s = np.sqrt(np.sum(resid ** 2) / dof)          # 残差标准差 (mV)

sig_a = s / np.sqrt(Sxx)
sig_b = s * np.sqrt(1.0 / n + Ebar ** 2 / Sxx)
r = stats.pearsonr(E, S)[0]
R2 = r ** 2

E0_fwd = (S0 - b) / a
# 逆回归的方差：标定曲线本身的不确定 + S0 作为单次测量的涨落
u_fwd = (s / abs(a)) * np.sqrt(1.0 + 1.0 / n + (S0 - Sbar) ** 2 / (a ** 2 * Sxx))

print('\n[1] 正向拟合   S = a*E + b')
print('  a = %.6f mV/keV   (标准误 %.6f)' % (a, sig_a))
print('  b = %.4f mV       (标准误 %.4f)' % (b, sig_b))
print('  r = %.6f,  R^2 = %.6f' % (r, R2))
print('  残差标准差 s = %.4f mV,  最大残差 = %.4f mV' % (s, np.max(np.abs(resid))))
print('  反解  E0 = (S0 - b)/a = %.2f keV' % E0_fwd)
print('  1 sigma 不确定度 = %.2f keV (相对 %.2f%%)'
      % (u_fwd, 100 * u_fwd / E0_fwd))
# 把 u_fwd 拆开看：单次测量项 s/|a| 与标定曲线项
u_single = s / abs(a)
u_calib = u_single * np.sqrt(1.0 / n + (S0 - Sbar) ** 2 / (a ** 2 * Sxx))
print('    其中 单次测量项 s/|a| = %.2f keV, 标定曲线项 = %.2f keV'
      % (u_single, u_calib))

# ----------------------------------------------------------------------
# 2. 反向拟合 E = p*S + q，直接给出 E0
# ----------------------------------------------------------------------
p, q = np.polyfit(S, E, 1)
E_fit = p * S + q
resid_E = E - E_fit
s_E = np.sqrt(np.sum(resid_E ** 2) / dof)      # 残差标准差 (keV)

sig_p = s_E / np.sqrt(Sss)
sig_q = s_E * np.sqrt(1.0 / n + Sbar ** 2 / Sss)

E0_rev = p * S0 + q
u_rev = s_E * np.sqrt(1.0 + 1.0 / n + (S0 - Sbar) ** 2 / Sss)

print('\n[2] 反向拟合   E = p*S + q')
print('  p = %.6f keV/mV   (标准误 %.6f)' % (p, sig_p))
print('  q = %.4f keV       (标准误 %.4f)' % (q, sig_q))
print('  E0 = p*S0 + q = %.2f keV' % E0_rev)
print('  1 sigma 不确定度 = %.2f keV (相对 %.2f%%)'
      % (u_rev, 100 * u_rev / E0_rev))

# ----------------------------------------------------------------------
# 3. 线性插值：取 S0 相邻的两个标定点
# ----------------------------------------------------------------------
lo = np.searchsorted(S, S0) - 1          # S 已按升序排列
E0_int = np.interp(S0, S[lo:lo + 2], E[lo:lo + 2])
print('\n[3] 线性插值   取 S = %d, %d mV 两点'
      % (S[lo], S[lo + 1]))
print('  E0 = %.2f keV' % E0_int)

# ----------------------------------------------------------------------
# 4. 结果汇总
# ----------------------------------------------------------------------
print('\n' + '=' * 62)
print('结果汇总')
print('-' * 62)
print('  %-28s %10s' % ('method', 'E0 (keV)'))
print('  %-28s %10.2f' % ('forward fit  S(E)', E0_fwd))
print('  %-28s %10.2f' % ('reverse fit  E(S)', E0_rev))
print('  %-28s %10.2f' % ('linear interpolation', E0_int))
print('  三种方法的最大差异 = %.2f keV'
      % (max(E0_fwd, E0_rev, E0_int) - min(E0_fwd, E0_rev, E0_int)))
print('=' * 62)
print('答案：待测粒子的能量约为 %.0f keV，即 %.3f MeV' % (E0_fwd, E0_fwd / 1000))
print('=' * 62)

# ----------------------------------------------------------------------
# 5. 绘图
# ----------------------------------------------------------------------
Eline = np.linspace(E.min() - 150, E.max() + 150, 200)

# 图 1：标定直线与反演结果
fig1, ax = plt.subplots(figsize=(7.2, 5.0))
ax.errorbar(E, S, yerr=s, fmt='o', color='#1f77b4', ms=6, capsize=3,
            label='calibration points ($\\pm s$)')
ax.plot(Eline, a * Eline + b, '-', color='#d62728', lw=1.8,
        label='forward fit: $S=%.4fE%.2f$' % (a, b))
for val, lab, col in [(E0_fwd, 'forward fit', '#d62728'),
                      (E0_rev, 'reverse fit', '#2ca02c'),
                      (E0_int, 'interpolation', '#9467bd')]:
    ax.axvline(val, ls=':', lw=1.2, color=col,
               label='$E_0$ (%s): %.0f keV' % (lab, val))
ax.axhline(S0, ls='--', lw=1.0, color='gray')
ax.plot([E0_fwd], [S0], '*', ms=15, color='k', zorder=5,
        label='$S_0=1502$ mV  $\\rightarrow$  $E_0$')
ax.set_xlabel('Energy $E$ (keV)')
ax.set_ylabel('Signal amplitude $S$ (mV)')
ax.set_title('Energy calibration of the $\\alpha$ detector')
ax.grid(alpha=0.3)
ax.legend(fontsize=8, loc='lower right')
fig1.tight_layout()
fig1.savefig('imgs/hw2_fit.png', dpi=200)
print('\n[saved] imgs/hw2_fit.png')

# 图 2：残差图
fig2, ax = plt.subplots(figsize=(7.2, 4.0))
ax.axhline(0, color='k', lw=1.0)
ax.errorbar(E, resid, yerr=s, fmt='o', color='#1f77b4', ms=6, capsize=3)
ax.plot(E, resid, '-', color='#1f77b4', lw=0.8, alpha=0.5)
for xi, ri in zip(E, resid):
    ax.annotate('%+.1f' % ri, (xi, ri), textcoords='offset points',
                xytext=(0, 9), ha='center', fontsize=8)
ax.set_xlabel('Energy $E$ (keV)')
ax.set_ylabel('Residual $S_i - (aE_i+b)$ (mV)')
ax.set_title('Residuals of the forward fit (std = %.2f mV)' % s)
ax.grid(alpha=0.3)
fig2.tight_layout()
fig2.savefig('imgs/hw2_residual.png', dpi=200)
print('[saved] imgs/hw2_residual.png')

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

# 各トンネルダイオードの電流-電圧特性
def I1(V1):
    return 0.43 * V1**3 - 2.69 * V1**2 + 4.56 * V1

def I2(V2):
    return 2.5 * V2**3 - 10.5 * V2**2 + 11.8 * V2

def I3(V3):
    return 1.3 * V3**3 - 5.4 * V3**2 + 6.9 * V3

# ホモトピー法による解法
def homotopy_method(V_total, R=1, num_steps=100):
    V_guess = [1.0, 1.0, 1.0]  # 初期推定値
    V_vals = []

    for step in np.linspace(0, 1, num_steps):
        # 前の解を使用して初期値を設定
        V_current = [V_guess[i] * (1 - step) + V_total * step for i in range(3)]
        
        # 方程式を解く
        V_solution = fsolve(circuit, V_current, args=(V_total,), xtol=1e-12)
        V_guess = V_solution  # 次のステップの初期推定値として更新

        V_vals.append(V_solution)

    return V_vals[-1]  # 最後の解を返す

# 回路方程式を定義
def circuit(V_vals, V_total, R=1):
    V1, V2, V3 = V_vals
    I = I1(V1)  # 各ダイオードの電流は同じと仮定
    return [
        V1 + V2 + V3 + I * R - V_total,  # 全体の電圧はV_totalに等しい
        I - I2(V2),                      # 各ダイオードの電流が一致する条件
        I - I3(V3)
    ]

# 電圧Vに対する電流Iを計算
V_vals_list = []
I_vals_list = []
V_total_range = np.linspace(0, 14, 100)  # 電圧範囲を0から14Vに設定

for V_total in V_total_range:
    V_solution = homotopy_method(V_total)
    V1, V2, V3 = V_solution
    I = I1(V1)  # 最終的な電流計算
    
    # 結果をリストに追加
    V_vals_list.append(V_total)
    I_vals_list.append(I)

# 結果をプロット
plt.plot(V_vals_list, I_vals_list, label='Homotopy Method', color='b')
plt.title('Driving Point Characteristic Curve (Homotopy Method)')
plt.xlabel('Voltage (V)')
plt.ylabel('Current (I)')
plt.legend()
plt.grid(True)
plt.show()

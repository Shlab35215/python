#include <stdio.h>
#include <math.h>

#define NUM_STEPS 100
#define NUM_V 5000
#define R 1.0

// 各トンネルダイオードの電流-電圧特性
double I1(double V1) {
    if (V1 < 0) return 0;  // 負の電圧に対する保護
    return 0.43 * pow(V1, 3) - 2.69 * pow(V1, 2) + 4.56 * V1;
}

// 回路方程式を解く関数
void circuit(double V_vals[3], double V_total, double result[3]) {
    double I = I1(V_vals[0]);  // 各ダイオードの電流は同じと仮定
    result[0] = V_vals[0] + V_vals[1] + V_vals[2] + I * R - V_total;  // 全体の電圧
    result[1] = I - I1(V_vals[1]);  // 各ダイオードの電流が一致する条件
}

// ニュートン法で非線形方程式を解く関数
void fsolve(double V_total, double result[3]) {
    double V_guess[3] = {1.0, 1.0, 1.0};  // 初期推定値
    for (int step = 0; step < NUM_STEPS; step++) {
        // 回路方程式を解く
        circuit(V_guess, V_total, result);
        for (int i = 0; i < 3; i++) {
            V_guess[i] += -result[i];  // 更新
        }
    }
}

// 主関数
int main() {
    double V_total_range[NUM_V];
    double I_vals[NUM_V];
    double result[3];

    // 電圧範囲を設定
    FILE *fp = fopen("data.txt", "w"); // データファイルのオープン
    for (int i = 0; i < NUM_V; i++) {
        V_total_range[i] = (double)i / (NUM_V - 1) * 14.0;  // 0から14Vに設定
        fsolve(V_total_range[i], result);
        I_vals[i] = I1(result[0]);  // 最終的な電流計算

        // 結果をファイルに書き込む
        fprintf(fp, "%.4f\t%.4f\n", V_total_range[i], I_vals[i]);
    }
    fclose(fp); // データファイルをクローズ

    return 0;
}

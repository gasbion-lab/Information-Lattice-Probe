import matplotlib.pyplot as plt
import numpy as np
import random
import math

def is_prime_miller_rabin(n, k_test=20):
    n = int(n)
    if n <= 1: return False
    if n <= 3: return True
    if n % 2 == 0: return False
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    for _ in range(k_test):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1: continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1: break
        else: return False
    return True

# --- 1. CONFIGURAZIONE GEOMETRICA ---
print("\n" + "="*55)
print("   MANIFOLD PROBE v4.9 - DIRICHLET INVARIANCE TEST")
print("="*55)
u_start = input("Coordinata Settore (Es. 2**201 o 10**100): ")
try:
    p_orig = int(eval(u_start))
except:
    p_orig = 10**20
scan_size = 5000 

# --- 2. SCANSIONE DEI CORRIDOI ---
print(f"Analisi invarianza su {scan_size} stati del lattice...")
counts = {1: 0, 5: 0, 7: 0, 11: 0}
punti_grafico = []

for p in range(p_orig, p_orig + scan_size):
    n_c = 2 * p + 1
    r12 = n_c % 12
    if r12 in counts:
        if is_prime_miller_rabin(n_c):
            counts[r12] += 1
            if len(punti_grafico) < 150: 
                punti_grafico.append((p, r12))

total_p = sum(counts.values())

# --- 3. VERIFICA EQUIDISTRIBUZIONE ---
print("\n" + "-"*45)
print(f"INVARIANZA NEI CANALI (MODULO 12)")
print("-" * 45)
for r in [1, 5, 7, 11]:
    perc = (counts[r] / total_p * 100) if total_p > 0 else 0
    status = "OK" if 20 < perc < 30 else "VAR"
    print(f"Canale {r:2d} mod 12: {counts[r]:4d} superstiti ({perc:.2f}%) [{status}]")
print("-" * 45)
print(f"Densità Totale Residua: {total_p/scan_size:.5f}")

# --- 4. VISUALIZZAZIONE DELLA RIGIDITÀ ---
plt.figure(figsize=(15, 7), facecolor='white')
mappa_y = {5: 1, 7: 2, 11: 4, 1: 5}
ampiezza_vista = 100

# Plotting dei punti di singolarità (Lime) e ostruzioni (Red)
for p in range(p_orig, p_orig + ampiezza_vista):
    r12 = (2*p + 1) % 12
    if r12 in mappa_y:
        x_pos = p - p_orig
        if is_prime_miller_rabin(2*p + 1):
            plt.scatter(x_pos, mappa_y[r12], edgecolors='lime', facecolors='none', 
                        s=120, linewidth=2, zorder=5, label='Singolarità' if x_pos==0 else "")
        else:
            plt.scatter(x_pos, mappa_y[r12], color='red', s=40, alpha=0.3, 
                        marker='x', label='Ostruzione Pencil' if x_pos==0 else "")

plt.title(f"MANIFOLD 12: Equidistribuzione Asintotica (Settore 10^{int(math.log10(p_orig))})\nInvarianza di Dirichlet: Canali bilanciati al ~25%")
plt.yticks([1, 2, 4, 5], ["Canale 5", "Canale 7", "Canale 11", "Canale 1"])
plt.xlabel(f"Offset dal punto di analisi (Base: {p_orig:.2e})")
plt.grid(True, axis='both', linestyle=':', alpha=0.3)
plt.ylim(0.5, 5.5)
plt.show()

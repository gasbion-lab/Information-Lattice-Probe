import matplotlib.pyplot as plt
import numpy as np
import random

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

# --- 1. CONFIGURAZIONE ---
print("\n" + "="*50)
print("   MANIFOLD PROBE v4.8 - STATISTICA DI DIRICHLET")
print("="*50)
u_start = input("Posizione p di partenza (Es. 2**201): ")
p_orig = int(eval(u_start))
scan_size = 5000 

# --- 2. SCANSIONE ---
print(f"Analisi statistica su {scan_size} posizioni...")
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

# --- 3. REPORT TESTUALE ---
print("\n" + "-"*40)
print(f"DISTRIBUZIONE NEI CORRIDOI (DIRICHLET)")
print("-" * 40)
for r in [1, 5, 7, 11]:
    perc = (counts[r] / total_p * 100) if total_p > 0 else 0
    print(f"Resto {r:2d} mod 12: {counts[r]:4d} superstiti ({perc:.2f}%)")
print("-" * 40)
print(f"Densità totale: {total_p}/{scan_size} ({total_p/scan_size:.4f})")

# --- 4. VISUALIZZAZIONE ---
plt.figure(figsize=(15, 7), facecolor='white')
mappa_y = {5: 1, 7: 2, 11: 4, 1: 5}
ampiezza_vista = 100

for p, r in punti_grafico:
    if p < p_orig + ampiezza_vista:
        plt.scatter(p - p_orig, mappa_y[r], edgecolors='lime', facecolors='none', s=100, linewidth=2, zorder=5)

for p in range(p_orig, p_orig + ampiezza_vista):
    r12 = (2*p + 1) % 12
    if r12 in mappa_y and not is_prime_miller_rabin(2*p+1):
        plt.scatter(p - p_orig, mappa_y[r12], color='red', s=30, alpha=0.4)

plt.title(f"ANALISI MANIFOLD: {p_orig:.2e}\nDistribuzione Dirichlet (Attesa: 25% per corridoio)")
plt.yticks([1, 2, 4, 5], ["Resto 5", "Resto 7", "Resto 11", "Resto 1"])
plt.xlabel("Offset locale (0-100)")
plt.grid(True, axis='x', linestyle=':', alpha=0.3)
plt.show()

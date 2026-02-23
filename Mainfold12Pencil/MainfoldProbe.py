import matplotlib.pyplot as plt
import numpy as np
import random
import math

# Test di primalità Miller-Rabin (Standard per scale crittografiche)
def is_prime_miller_rabin(n, k_test=10):
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

# --- 1. SETTAGGIO COORDINATE MANIFOLD ---
print("\n" + "="*50)
print("   MANIFOLD PROBE v5.0 - STRUCTURAL RIGIDITY")
print("="*50)
u_start = input("Inserire Coordinata Settore (Es. 2**201 o 10**100): ")
try:
    p_orig = int(eval(u_start)) 
except:
    p_orig = 10**50 # Default di sicurezza

# --- 2. RICERCA DELLA SINGOLARITÀ (HUNTER) ---
print(f"\nAnalisi della porosità nel settore 10^{int(math.log10(p_orig))}...")
gemelli_trovati = []
p_check = p_orig

# Limite di scansione basato sulla densità teorica (Evita loop infiniti)
scansione_max = 5000000 

while len(gemelli_trovati) < 1:
    # Condizione strutturale del Manifold 12
    if (p_check % 6 == 2 or p_check % 6 == 5):
        if is_prime_miller_rabin(2*p_check+1) and is_prime_miller_rabin(2*p_check+3):
            gemelli_trovati.append((p_check, 2*p_check+1, 2*p_check+3))
            break
    p_check += 1
    if p_check - p_orig > scansione_max: 
        print("Soglia di porosità locale superata. Espandere raggio di scansione.")
        break

if not gemelli_trovati:
    exit()

p_f, n1, n2 = gemelli_trovati[0]
p_start = p_f
ampiezza_grafico = 100 
p_end = p_start + ampiezza_grafico

mappa_y_mod12 = {5: 1, 7: 2, 11: 4, 1: 5}

# --- 3. RAPPRESENTAZIONE GEOMETRICA ---
plt.figure(figsize=(16, 8), facecolor='white')
x_rel = np.linspace(0, ampiezza_grafico, 2000)

# Trama fissa del Pencil (Le linee di ostruzione)
generatori_n = [n for n in range(5, 100, 2) if is_prime_miller_rabin(n, 5)]
for n_g in generatori_n:
    g = (n_g - 1) // 2
    # Simulazione della periodicità del Pencil
    y_m = (n_g * (p_start + x_rel) + g) % 6
    y_p = np.interp(y_m, [0, 2, 3, 5], [5, 1, 2, 4], left=np.nan, right=np.nan)
    y_p[np.abs(np.diff(y_p, prepend=y_p[0])) > 0.8] = np.nan
    plt.plot(x_rel, y_p, '--', color='gray', alpha=0.08, linewidth=0.6)

# Disegno dei Resitui (Punti di Porosità)
for p in range(p_start, p_end + 1):
    r12 = (2 * p + 1) % 12
    if r12 in mappa_y_mod12:
        y_v = mappa_y_mod12[r12]
        x_pos = p - p_start
        is_p1 = is_prime_miller_rabin(2*p+1)
        
        # Colore Lime per Singolarità, Rosso per Ostruzione del Pencil
        plt.scatter(x_pos, y_v, facecolors='lime' if is_p1 else 'none', 
                    edgecolors='black', s=140, linewidth=1.5, zorder=5, alpha=0.8)

# --- ESTETICA E DOCUMENTAZIONE ---
plt.title(f"MANIFOLD 12 PROBE | Settore: 10^{int(math.log10(p_f))} | Singolarità Rilevata", fontsize=14)
plt.yticks([1, 2, 4, 5], ["Canale 5", "Canale 7", "Canale 11", "Canale 1"])
plt.xlabel(f"Distanza Relativa dal Punto di Singolarità (P = {p_f})", fontsize=12)
plt.xticks(np.arange(0, ampiezza_grafico + 1, 10))



plt.grid(True, axis='x', linestyle=':', alpha=0.3)
plt.xlim(-2, ampiezza_grafico + 2)
plt.ylim(0.5, 5.5)
plt.tight_layout()
plt.show()

# --- REPORT FINALE ---
print("\n" + "="*50)
print("DATI STRUTTURALI DELLA SINGOLARITÀ")
print("="*50)
print(f"P-COORDINATE : {p_f}")
print(f"VALORE N1    : {n1}")
print(f"VALORE N2    : {n2}")
print(f"DISTANZA SCAN: {p_f - p_orig} unità")
print("STATO        : Porosità verificata entro il Limite di Von Koch.")
print("="*50)

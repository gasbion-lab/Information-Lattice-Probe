import matplotlib.pyplot as plt
import numpy as np
import random
import math

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

# --- 1. INPUT ---
print("\n" + "="*40)
print("   MANIFOLD PROBE v4.7 - PURE GEOMETRY")
print("="*40)
u_start = input("Posizione p di partenza (Es. 2**201): ")
try:
    p_orig = int(eval(u_start)) 
except:
    p_orig = 22

# --- 2. RICERCA HUNTER ---
print(f"\nRicerca in corso nel Manifold...")
gemelli_trovati = []
p_check = p_orig

while len(gemelli_trovati) < 1:
    if (p_check % 6 == 2 or p_check % 6 == 5):
        if is_prime_miller_rabin(2*p_check+1) and is_prime_miller_rabin(2*p_check+3):
            gemelli_trovati.append((p_check, 2*p_check+1, 2*p_check+3))
            break
    p_check += 1
    if p_check - p_orig > 20000000: break

p_found = gemelli_trovati[0][0] if gemelli_trovati else p_orig
p_start = p_found
ampiezza_grafico = 100 
p_end = p_start + ampiezza_grafico

mappa_y_mod12 = {5: 1, 7: 2, 11: 4, 1: 5}

# --- 3. DISEGNO ---
plt.figure(figsize=(16, 8), facecolor='white')
x_rel = np.linspace(0, ampiezza_grafico, 2000)

# Fascio di rette (trama fissa k=51 per riferimento strutturale)
generatori_n = [n for n in range(5, 104, 2) if is_prime_miller_rabin(n, 5)]
for i, n_g in enumerate(generatori_n):
    g = (n_g - 1) // 2
    y_m = (n_g * (p_start + x_rel) + g) % 6
    y_p = np.interp(y_m, [0, 2, 3, 5], [5, 1, 2, 4], left=np.nan, right=np.nan)
    y_p[np.abs(np.diff(y_p, prepend=y_p[0])) > 0.8] = np.nan
    plt.plot(x_rel, y_p, '--', color='gray', alpha=0.1, linewidth=0.8)

# Disegno Punti (Offset rimosso, solo indici 0-100)
for p in range(p_start, p_end + 1):
    r12 = (2 * p + 1) % 12
    if r12 in mappa_y_mod12:
        y_v = mappa_y_mod12[r12]
        x_pos = p - p_start
        is_p1 = is_prime_miller_rabin(2*p+1)
        plt.scatter(x_pos, y_v, facecolors='none' if is_p1 else 'red', 
                    edgecolors='lime' if is_p1 else 'black', 
                    s=130, linewidth=2, zorder=5)

# --- TITOLO E ASSI ---
p_f, n1, n2 = gemelli_trovati[0]
plt.title(f"MANIFOLD PROBE | Settore Locale [Gemello + 100] | $k_{{max}} \\approx \\sqrt{{x}}$", fontsize=14, fontweight='bold')
plt.yticks([1, 2, 4, 5], ["Resto 5", "Resto 7", "Resto 11", "Resto 1"])
plt.xlabel((f"DISTANZA DAL PUNTO ORIGINALE: {p_f - p_orig}"), fontsize=12)

# Asse X pulito: solo tacche da 0 a 100
plt.xticks(np.arange(0, ampiezza_grafico + 1, 10))

plt.grid(True, axis='x', linestyle=':', alpha=0.3)
plt.xlim(-2, ampiezza_grafico + 2)
plt.ylim(0.5, 5.5)
plt.tight_layout()
plt.show()

# --- REPORT IDLE ---
print("\n" + "="*60)
print("DATI DETTAGLIATI (IDLE)")
print("="*60)
if gemelli_trovati:
    print(f"POSIZIONE ORIGINALE: {p_orig}")
    p_f, n1, n2 = gemelli_trovati[0]
    print(f"POSIZIONE P del Primo Gemello : {p_f}")
    print(f"PRIMO NUMERO (2p+1) : {n1}")
    print(f"SECONDO NUMERO (2p+3): {n2}")
    print(f"DISTANZA DAL PUNTO ORIGINALE: {p_f - p_orig}")
else:
    print("Nessuna coppia trovata.")
print("="*60)

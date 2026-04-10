import random
import math
import time
import matplotlib.pyplot as plt
import numpy as np
# Developed by Gasbion-lab | Part of the Information Lattice Field Theory (ILFT)
# --- MOTORE DI CALCOLO ---
def miller_rabin(n, k=40):
    if n <= 1: return False
    if n <= 3: return True
    if n % 2 == 0: return False
    r, d = 0, n - 1
    while d % 2 == 0: r += 1; d //= 2
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1: continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1: break
        else: return False
    return True

def get_huge_k(exp):
    PREC = 10**25
    pi_p = int(math.pi * PREC)
    ln10_p = int(math.log(10) * PREC)
    ln_2pie_p = int(math.log(2 * math.pi * math.e) * PREC)
    t = 10**exp
    ln_t_p = exp * ln10_p
    num = t * (ln_t_p - ln_2pie_p)
    den = 2 * pi_p
    return num // den

# --- ANALISI GUE (CORRETTA) ---
def plot_gue_distribution(found_k_steps, exp):
    if len(found_k_steps) < 3:
        print("\n[!] Dati insufficienti per il test GUE (servono almeno 3 distanze).")
        return
    
    # Calcoliamo le distanze tra i passi k in cui abbiamo trovato i gemelli
    steps = np.sort(found_k_steps)
    spacings = np.diff(steps)
    
    # Se tutte le distanze sono uguali, non possiamo fare statistica
    if np.all(spacings == spacings[0]) and len(spacings) < 5:
        print("\n[!] Le distanze sono troppo uniformi per mostrare una curva GUE.")
        return

    # Normalizzazione: S = spaziatura / media_spaziature
    mean_s = np.mean(spacings)
    s = spacings / mean_s

    plt.figure(figsize=(10, 6))
    # Istogramma
    plt.hist(s, bins=10, density=True, alpha=0.5, color='royalblue', label='Distanze Gemelli (Tua Retta)')
    
    # Curva GUE Teorica (Wigner)
    x = np.linspace(0, 3, 100)
    p_gue = (32 / (np.pi**2)) * (x**2) * np.exp(-4 * (x**2) / np.pi)
    plt.plot(x, p_gue, 'r-', lw=2, label='Firma GUE (Zeta di Riemann)')

    plt.title(f"Test Repulsione degli Zeri - Quota 10^{exp}")
    plt.xlabel("Distanza Normalizzata (s)")
    plt.ylabel("Densità di Probabilità")
    plt.legend()
    plt.grid(True, alpha=0.2)
    plt.show()

# --- RICERCA ---
def main_zeta_experiment():
    print("=== TELESCOPIO ZETA: FIX GUE SPACING ===")
    exp = int(input("Esponente quota Zeta (es. 100): "))
    steps = int(input("Numero di passi (consigliato 50000): "))

    start_k = get_huge_k(exp)
    found_k_relative = [] # Memorizziamo il passo 'i' del ritrovamento
    start_time = time.time()

    print(f"\nScansione in corso a 10^{exp}...")
    
    for i in range(1, steps + 1):
        k = start_k + i
        # Controllo fessure 11-13 e 17-19
        for offset in [11, 17]:
            if miller_rabin(180*k + offset) and miller_rabin(180*k + offset + 2):
                found_k_relative.append(i)
                print(f"🌟 [Passo {i}] Gemelli trovati!")

    print(f"\n--- FINE SCANSIONE ---")
    print(f"Coppie trovate: {len(found_k_relative)}")
    
    if len(found_k_relative) >= 3:
        plot_gue_distribution(found_k_relative, exp)
    else:
        print("Cerca ancora, servono più punti per il grafico GUE.")

if __name__ == "__main__":
    main_zeta_experiment()

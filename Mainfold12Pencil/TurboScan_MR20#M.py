import random
import time
import math

def miller_rabin(n, k=7):
    if n < 2: return False
    if n == 2 or n == 3: return True
    if n % 2 == 0: return False
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1: continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1: break
        else: return False
    return True

def get_primes(count):
    primes = []
    n = 2
    while len(primes) < count:
        is_p = True
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                is_p = False
                break
        if is_p: primes.append(n)
        n += 1
    return primes

def run_consistency_check(quota, p_list, n_windows=20, steps_per_window=5000):
    step = 1
    for p in p_list: step *= p
    
    results = []
    print(f"--- VERIFICA CONSISTENZA P{len(p_list)}# ---")
    print(f"Passo Primoriale: ~10^{int(math.log10(step))}")
    print(f"Campione: {n_windows} finestre da {steps_per_window} passi ciascuna")
    print("-" * 50)
    
    current_search = quota
    for w in range(n_windows):
        ancora = None
        search_start = current_search + (11 - (current_search % 6)) % 6
        # Ricerca ancora lineare per ogni finestra
        for i in range(1000000):
            n = search_start + (i * 6)
            if miller_rabin(n) and miller_rabin(n + 2):
                ancora = n
                break
        
        if ancora:
            count = 1
            for i in range(1, steps_per_window):
                if miller_rabin(ancora + (i * step)) and miller_rabin(ancora + (i * step) + 2):
                    count += 1
            results.append(count)
            print(f"Finestra {w+1:02}/20 | Ancora trovata | Coppie: {count}")
            # Sposta la ricerca di 1 milione di unità per la prossima finestra
            current_search = ancora + 1000000
        else:
            print(f"Finestra {w+1:02}/20 | Ancora NON trovata")
            
    return results

# --- CONFIGURAZIONE ---
quota_googol = 10**100
n_primi = 20
n_finestre = 20
passi_finestra = 5000
baseline_linear_eff = 0.0025 # 0.0025% media spaziale

# Esecuzione
prime_pool = get_primes(n_primi)
data_points = run_consistency_check(quota_googol, prime_pool, n_finestre, passi_finestra)

# Analisi Statistica
if data_points:
    media_coppie = sum(data_points) / len(data_points)
    efficienza_media = (media_coppie / passi_finestra) * 100
    gain_reale = efficienza_media / baseline_linear_eff
    dev_std = math.sqrt(sum((x - media_coppie)**2 for x in data_points) / len(data_points))

    print("\n" + "="*50)
    print("REPORT FINALE DI CORRELAZIONE (P20#)")
    print("="*50)
    print(f"Media coppie rilevate:   {media_coppie:.2f}")
    print(f"Efficienza Media:        {efficienza_media:.4f}%")
    print(f"GAIN SISTEMICO:          {gain_reale:.1f}x (rispetto a media lineare)")
    print(f"Stabilità (Dev. Std):    {dev_std:.2f}")
    print(f"Intervallo Min/Max:      {min(data_points)} / {max(data_points)}")
    print("="*50)

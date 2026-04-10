import random
# Developed by Gasbion-lab | Part of the Information Lattice Field Theory (ILFT)
def is_prime(n, k=25): 
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

def analyze_porosity(start_scale, num_windows=50, window_size=20000):
    results = []
    print(f"Analisi su {num_windows} intervalli da {window_size} numeri...")
    
    for i in range(num_windows):
        current_start = start_scale + (i * window_size)
        twins = 0
        for n in range(current_start, current_start + window_size - 2):
            if is_prime(n) and is_prime(n + 2):
                twins += 1
        results.append(twins)
        if (i+1) % 10 == 0: print(f"Completati {i+1}/{num_windows} intervalli...")

    mean = sum(results) / num_windows
    variance = sum((x - mean) ** 2 for x in results) / num_windows
    std_dev = variance ** 0.5
    
    print("\n--- RISULTATI ANALISI ---")
    print(f"Scala Iniziale: {start_scale}")
    print(f"Media coppie gemelle: {mean:.2f}")
    print(f"Deviazione Standard (Rumore): {std_dev:.2f}")
    print(f"Valore Min/Max trovati: {min(results)} / {max(results)}")
    return results

data = analyze_porosity(10**9)

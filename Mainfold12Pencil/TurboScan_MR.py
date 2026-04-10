import random
import time
# Developed by Gasbion-lab | Part of the Information Lattice Field Theory (ILFT)
def miller_rabin(n, k=27):
    if n < 2: return False
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

def is_candidate(n):
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]:
        if n % p == 0: return n == p
    return True

def deep_scan_100(num_windows=50, window_size=2000000):
    start_scale = 10**100
    results = []
    print(f"--- TURBO SCAN QUOTA 10^100 ---")
    print(f"Analisi di {num_windows} intervalli da {window_size} numeri ciascuno...")
    
    start_time = time.time()
    
    for i in range(num_windows):
        win_start = start_scale + (i * window_size)
        twins = 0
        for n in range(win_start + 1 if win_start % 2 == 0 else win_start, win_start + window_size - 2, 2
            if is_candidate(n) and is_candidate(n+2):
                if miller_rabin(n) and miller_rabin(n+2):
                    twins += 1
        
        results.append(twins)
        elapsed = time.time() - start_time
        print(f"Intervallo {i+1}/{num_windows} | Gemelli: {twins} | Tempo parziale: {elapsed:.1f}s")

    mean = sum(results) / num_windows
    variance = sum((x - mean) ** 2 for x in results) / num_windows
    std_dev = variance ** 0.5
    
    print("\n--- RISULTATI FINALI QUOTA 10^100 ---")
    print(f"Media coppie gemelle su {window_size} numeri: {mean:.2f}")
    print(f"Deviazione Standard: {std_dev:.2f}")
    print(f"Rapporto Rumore/Media: {(std_dev/mean)*100:.1f}%")
    return results

data_100 = deep_scan_100()

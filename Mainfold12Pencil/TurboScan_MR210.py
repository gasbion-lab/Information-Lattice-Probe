import random
import time
import matplotlib.pyplot as plt
# Developed by Gasbion-lab | Part of the Information Lattice Field Theory (ILFT)
def miller_rabin(n, k=7):
    if n < 2: return False
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

def run_detailed_scan(quota, resto, passo, target_distanza):
    start_total = time.time()
    numero_salti = target_distanza // passo
    n_partenza = quota + (resto - (quota % passo)) % passo
    
    print(f"\n" + "="*50)
    print(f"TEST CORRIDOIO: Passo {passo} | Distanza Target: {target_distanza}")
    
    # 1. Ricerca Ancora
    start_anchor = time.time()
    ancora = None
    for i in range(2000000):
        n = n_partenza + (i * passo)
        if miller_rabin(n) and miller_rabin(n + 2):
            ancora = n
            break
    anchor_time = time.time() - start_anchor
    
    if ancora is None:
        print("Errore: Ancora non trovata.")
        return 0, 0, 0

    print(f"Ancora trovata a: 10^100 + {ancora - quota}")
    print(f"Tempo ricerca ancora: {anchor_time:.2f}s")
    
    # 2. Scansione
    print(f"Esecuzione di {numero_salti} salti...")
    coppie = 1
    start_scan = time.time()
    for i in range(1, numero_salti):
        if miller_rabin(ancora + (i * passo)) and miller_rabin(ancora + (i * passo) + 2):
            coppie += 1
    
    scan_time = time.time() - start_scan
    efficienza = (coppie / numero_salti) * 100
    total_time = time.time() - start_total
    
    print(f"Risultato: {coppie} coppie trovate.")
    print(f"Efficienza per passo: {efficienza:.4f}%")
    print(f"Tempo totale: {total_time:.2f}s")
    
    return coppie, efficienza, numero_salti

# --- PARAMETRI ---
quota = 10**100
distanza = 3000000
baseline_linear = 0.0025

# Esecuzione Scansioni
c60, e60, s60 = run_detailed_scan(quota, 11, 60, distanza)
c90, e90, s90 = run_detailed_scan(quota, 17, 90, distanza)
c210, e210, s210 = run_detailed_scan(quota, 11, 210, distanza)

# --- GENERAZIONE FIGURA 9 ---
labels = ['Linear\n(Baseline)', 'Step 60\n(12x5)', 'Step 90\n(12x7.5)', 'Step 210\n(Primorial)']
effs = [baseline_linear, e60, e90, e210]
colors = ['#808080', '#3498db', '#27ae60', '#f1c40f']

plt.figure(figsize=(10, 6))
bars = plt.bar(labels, effs, color=colors, alpha=0.85)

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.001, f'{yval:.4f}%', 
             ha='center', fontweight='bold', fontsize=10)

plt.title(f'Figure 9: Hit-Rate Efficiency Comparison at $10^{{100}}$\n(Normalized Distance: {distanza} units)', fontsize=12, fontweight='bold')
plt.ylabel('Success Probability per Attempt (%)')
plt.grid(axis='y', linestyle='--', alpha=0.3)
plt.ylim(0, max(effs) * 1.3)
plt.tight_layout()
plt.savefig('figura9_primorial.png', dpi=300)
plt.show()

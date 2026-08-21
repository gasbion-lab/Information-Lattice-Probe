import math
import warnings
import logging
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")
logging.getLogger('matplotlib').setLevel(logging.ERROR)

def miller_rabin(n, k=5):
    """Test di primalità di Miller-Rabin."""
    if n < 2: return False
    if n in (2, 3): return True
    if n % 2 == 0: return False
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    for _ in range(k):
        a = 2 + (int(math.log2(n)) * 123456789) % (n - 3) if n > 4 else 2
        if a >= n - 1: a = 2
        x = pow(a, d, n)
        if x == 1 or x == n - 1: continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1: break
        else: return False
    return True

def scansiona_fascio_rette(H):
    M = 2 * H + 1
    sqrt_M = math.sqrt(M)
    
    print(f"\n--- ANALISI GEOMETRICA FONDATA SU X ---")
    print(f"Quota H = {H}")
    print(f"M = 2H + 1 = {M}")
    print(f"Radice quadrata di M (sqrt(M)) = {sqrt_M:.2f}")
    
    if miller_rabin(M):
        print(f"[INFO] M = {M} è un numero PRIMO. Nessuna intersezione.")
        return

    tutti_i_punti = []
    limite_m = int(sqrt_M)
    
    for m in range(5, limite_m + 1):
        resto = m % 6
        if resto != 1 and resto != 5:
            continue
            
        x_float = (M - m) / (2 * m)
        if x_float.is_integer():
            x1 = int(x_float)
            p1 = 2 * x1 + 1
            q1 = M // p1
            
            coppie = [
                (x1, p1, q1),
                ((q1 - 1) // 2, q1, p1)
            ]
            
            for cx, cp, cq in coppie:
                if cx > 0 and not any(p['x'] == cx for p in tutti_i_punti):
                    tutti_i_punti.append({
                        'x': cx,
                        'p1': cp,
                        'primo_p1': miller_rabin(cp),
                        'q1': cq,
                        'primo_q1': miller_rabin(cq)
                    })

    if not tutti_i_punti: 
        print("[INFO] Nessuna intersezione geometrica trovata.")
        return

    tutti_i_punti = sorted(tutti_i_punti, key=lambda k: k['x'])

    print(f"[INFO] Trovate {len(tutti_i_punti)} intersezioni geometriche (ordinate dal basso per X):")
    for p in tutti_i_punti:
        print(f"  -> X = {p['x']} | p1 = {p['p1']} (Primo: {p['primo_p1']}) | q1 = {p['q1']} (Primo: {p['primo_q1']})")

    # Visualizzazione grafica
    num_collisioni = len(tutti_i_punti)
    cols = min(6, num_collisioni)
    rows = math.ceil(num_collisioni / cols)
    fig, assi = plt.subplots(rows, cols, squeeze=False, figsize=(3.8 * cols, 3.2 * rows))
    fig.subplots_adjust(wspace=0.4, hspace=0.8)
    assi_piatti = assi.flatten()

    for idx, p in enumerate(tutti_i_punti):
        ax = assi_piatti[idx]
        colore_led_p1 = '#00E5FF' if p['primo_p1'] else '#FFEA00'
        colore_led_q1 = '#00E5FF' if p['primo_q1'] else '#FFEA00'
        
        sfondo_sup = plt.Rectangle((p['x']-3.5, 0.1), 7, 0.7, facecolor='black', edgecolor='none')
        sfondo_inf = plt.Rectangle((p['x']-3.5, -0.8), 7, 0.7, facecolor='black', edgecolor='none')
        ax.add_patch(sfondo_sup); ax.add_patch(sfondo_inf)
        
        rect_sup = plt.Rectangle((p['x']-0.4, 0.15), 0.8, 0.6, facecolor=colore_led_p1, edgecolor='white')
        rect_inf = plt.Rectangle((p['x']-0.4, -0.75), 0.8, 0.6, facecolor=colore_led_q1, edgecolor='white')
        ax.add_patch(rect_sup); ax.add_patch(rect_inf)
        
        testo_p1 = f"{p['p1']}" if p['p1'] < 1000000 else f"{p['p1']:.2e}"
        testo_q1 = f"{p['q1']}" if p['q1'] < 1000000 else f"{p['q1']:.2e}"
        
        ax.text(p['x'], 1.0, f"X={p['x']}\np1={testo_p1}\nq1={testo_q1}", ha='center', fontsize=6, fontweight='bold', bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))
        
        ax.set_xlim(p['x']-4, p['x']+4)
        ax.set_ylim(-1.5, 2.5)
        ax.axis('off')

    for j in range(num_collisioni, len(assi_piatti)): assi_piatti[j].set_visible(False)
    plt.suptitle(f'Analisi Fascio di Rette H={H}', fontsize=12)
    plt.show()

def main():
    while True:
        val = input("\nInserisci H (o 'esci'): ")
        val = val.strip()
        if val.lower() == 'esci': break
        try: scansiona_fascio_rette(int(val))
        except ValueError: print("Inserisci un numero valido.")

if __name__ == "__main__":
    main()

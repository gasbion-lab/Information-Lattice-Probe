import math
import warnings
import logging

warnings.filterwarnings("ignore")
logging.getLogger('matplotlib').setLevel(logging.ERROR)

def miller_rabin(n, k=5):
    """Test di primalità di Miller-Rabin ottimizzato e sicuro per numeri grandi."""
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
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def scansiona_fascio_rette(H):
    M = 2 * H + 1
    sqrt_H = math.sqrt(H)
    sqrt_M = math.sqrt(M)
    
    print(f"\n--- ANALISI GEOMETRICA CON FASCIO DI RETTE ---")
    print(f"Quota H = {H} (sqrt(H) = {sqrt_H:.2f})")
    print(f"M = 2H + 1 = {M} (sqrt(M) = {sqrt_M:.2f})")
    
    if miller_rabin(M):
        print(f"[INFO] M = {M} è un numero PRIMO. Nessuna intersezione geometrica interna.")
        return

    print("[INFO] Scansione delle intersezioni del fascio di rette basata su sqrt(H)...")
    tutti_i_punti = []
    
    # Limite di X basato sulla radice di H (o esteso per coprire l'intervallo geometrico)
    limite_x = int(sqrt_H) * 2 + 10
    
    limite_M = int(sqrt_M)
    for x in range(1, limite_M + 1):
        p1 = 2 * x + 1
        if M % p1 == 0:
            q1 = M // p1
            
            primo_p1 = miller_rabin(p1)
            primo_q1 = miller_rabin(q1)
            
            resto = p1 % 6
            tipo_resto = "+1" if resto == 1 else ("+5" if resto == 5 else "base")
            
            tutti_i_punti.append({
                'x': x,
                'p1': p1,
                'primo_p1': primo_p1,
                'q1': q1,
                'primo_q1': primo_q1,
                'tipo_resto': tipo_resto
            })

    if not tutti_i_punti: 
        print("[INFO] Nessuna intersezione geometrica trovata.")
        return

    num_collisioni = len(tutti_i_punti)
    print(f"[INFO] Trovate {num_collisioni} intersezioni geometriche. Apertura grafico...")
    
    
    for p in tutti_i_punti:
        print(f"  -> X={p['x']} | 2x+1 = {p['p1']} | Simmetrico k = {p['q1']}")

    import matplotlib.pyplot as plt

    cols = min(6, num_collisioni)
    rows = math.ceil(num_collisioni / cols)

    fig, assi = plt.subplots(rows, cols, squeeze=False, figsize=(3.8 * cols, 3.2 * rows))
    fig.subplots_adjust(wspace=0.4, hspace=0.8)

    assi_piatti = assi.flatten()

    for idx, p in enumerate(tutti_i_punti):
        ax = assi_piatti[idx]
        x_target = p['x']
        p1 = p['p1']
        q1 = p['q1']
        primo_p1 = p['primo_p1']
        primo_q1 = p['primo_q1']
        tipo_resto = p['tipo_resto']
        
        colore_led_p1 = '#00E5FF' if primo_p1 else '#FFEA00'
        colore_led_q1 = '#00E5FF' if primo_q1 else '#FFEA00'
        
        intorno_min = x_target - 3
        intorno_max = x_target + 3
        
        sfondo_sup = plt.Rectangle((intorno_min - 0.5, 0.1), 7, 0.7, facecolor='black', edgecolor='none', zorder=1)
        sfondo_inf = plt.Rectangle((intorno_min - 0.5, -0.8), 7, 0.7, facecolor='black', edgecolor='none', zorder=1)
        ax.add_patch(sfondo_sup)
        ax.add_patch(sfondo_inf)
        
        for x_intorno in range(intorno_min, intorno_max + 1):
            if x_intorno == x_target:
                rect_sup = plt.Rectangle((x_intorno - 0.4, 0.15), 0.8, 0.6, facecolor=colore_led_p1, edgecolor='white', linewidth=1.2, zorder=2)
                ax.add_patch(rect_sup)
                rect_inf = plt.Rectangle((x_intorno - 0.4, -0.75), 0.8, 0.6, facecolor=colore_led_q1, edgecolor='white', linewidth=1.2, zorder=2)
                ax.add_patch(rect_inf)
            else:
                rect_sup = plt.Rectangle((x_intorno - 0.4, 0.15), 0.8, 0.6, facecolor='black', edgecolor='#333333', linewidth=0.4, zorder=1)
                rect_inf = plt.Rectangle((x_intorno - 0.4, -0.75), 0.8, 0.6, facecolor='black', edgecolor='#333333', linewidth=0.4, zorder=1)
                ax.add_patch(rect_sup)
                ax.add_patch(rect_inf)

        testo_p1 = f"{p1}" if p1 < 1000000 else f"{p1:.2e}"
        testo_q1 = f"{q1}" if q1 < 1000000 else f"{q1:.2e}"
        
        ax.text(x_target, 1.0, f'X={x_target} (M6:{tipo_resto})\n2x+1={testo_p1}\nk={testo_q1}', ha='center', va='bottom', 
               fontsize=6, fontweight='bold', color='black',
               bbox=dict(boxstyle='round,pad=0.25', facecolor='white', alpha=0.95), zorder=3)

        ax.set_xlim(intorno_min - 0.6, intorno_max + 0.6)
        ax.set_ylim(-1.3, 2.7)
        ax.get_yaxis().set_visible(False)
        ax.set_aspect('equal')
        
        ax.set_xticks([x_target])
        ax.tick_params(axis='x', labelsize=7)

    for j in range(num_collisioni, len(assi_piatti)):
        assi_piatti[j].set_visible(False)

    plt.suptitle(f'Intersezioni del Fascio di Rette alla Quota H={H}\n[Superiore = 2x+1 | Inferiore = Simmetrico k | AZZURRO = Primo, GIALLO = Composto]', fontsize=9, y=0.98)
    plt.show()

def main():
    print("=== SCANNER GEOMETRICO ===")
    while True:
        try:
            input_utente = input("\nInserisci la quota H (o scrivi 'esci' per terminare): ").strip()
            if input_utente.lower() == 'esci':
                break
            if not input_utente:
                continue
            
            H_scelta = int(input_utente)
            if H_scelta < 0:
                print("Inserisci un numero positivo.")
                continue
                
            scansiona_fascio_rette(H_scelta)
        except ValueError:
            print("[ERRORE] Inserisci un numero intero valido.")
        except KeyboardInterrupt:
            print("\nUscita dal programma.")
            break

if __name__ == "__main__":
    main()


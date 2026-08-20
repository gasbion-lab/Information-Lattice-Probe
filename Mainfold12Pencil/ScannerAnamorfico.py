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

def scansiona_e_genera_intorni_led(H):
    M = 2 * H + 1
    print(f"\n--- ANALISI QUOTA H = {H} (M = {M}) ---")
    
    # 1. CONTROLLO PRELIMINARE: Se M è primo, evitiamo calcoli a vuoto
    if miller_rabin(M):
        print(f"[INFO] M = {M} è un numero PRIMO. Non esistono fattori non banali.")
        return

    print("[INFO] Il numero è composto. Avvio ricerca intersezioni geometriche...")
    colore_pixel = {}
    
    # 2. Ricerca dei divisori vincolati al Modulo 6
    for i in range(1, int(math.sqrt(M)) + 1, 2):
        if M % i == 0:
            divisori = [i, M // i]
            for denominatore in divisori:
                if denominatore == 1 or denominatore == M:
                    continue
                
                resto = denominatore % 6
                if resto == 1 or resto == 5 or denominatore <= 5:
                    x = (denominatore - 1) // 2
                    k = M // denominatore
                    if k > 0:
                        es_primo = miller_rabin(k)
                        tipo_resto = "+1" if resto == 1 else ("+5" if resto == 5 else "base")
                        colore_pixel[x] = (k, es_primo, tipo_resto)
                        print(f"[INTERSEZIONE X={x}] Divisore={denominatore} (Mod 6: {resto}) -> Pendenza k = {k} (Primo: {es_primo})")

    if not colore_pixel: 
        print("[INFO] Nessun fattore trovato che rispetti il filtro geometrico del modulo 6.")
        return

    coordinate_attive = sorted(list(colore_pixel.keys()))
    num_collisioni = len(coordinate_attive)

    import matplotlib.pyplot as plt

    # --- GENERATORE DI MATRICE GRAFICA MULTI-RIGA PER EVITARE SOVRAPPOSIZIONI ---
    cols = min(6, num_collisioni)
    rows = math.ceil(num_collisioni / cols)

    fig, assi = plt.subplots(rows, cols, squeeze=False, figsize=(3.5 * cols, 2.8 * rows))
    fig.subplots_adjust(wspace=0.4, hspace=0.7)

    assi_piatti = assi.flatten()

    for idx, x_target in enumerate(coordinate_attive):
        ax = assi_piatti[idx]
        k, es_primo, tipo_resto = colore_pixel[x_target]
        colore_led = '#00E5FF' if es_primo else '#FFEA00' # Azzurro (Primo) o Giallo (Composto)
        
        intorno_min = x_target - 3
        intorno_max = x_target + 3
        
        sfondo = plt.Rectangle((intorno_min - 0.5, -0.4), 7, 0.8, facecolor='black', edgecolor='none', zorder=1)
        ax.add_patch(sfondo)
        
        for x_intorno in range(intorno_min, intorno_max + 1):
            if x_intorno == x_target:
                rect = plt.Rectangle((x_intorno - 0.4, -0.4), 0.8, 0.8, facecolor=colore_led, edgecolor='white', linewidth=1.5, zorder=2)
                ax.add_patch(rect)
                
                testo_k = f"{k}" if k < 1000000 else f"{k:.3e}"
                # Testo disposto su più righe per leggibilità pulita
                ax.text(x_target, 0.55, f'X={x_target}\nk={testo_k}\n(M6:{tipo_resto})', ha='center', va='bottom', 
                       fontsize=6.5, fontweight='bold', color='black',
                       bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.9), zorder=3)
            else:
                rect = plt.Rectangle((x_intorno - 0.4, -0.4), 0.8, 0.8, facecolor='black', edgecolor='#333333', linewidth=0.5, zorder=1)
                ax.add_patch(rect)

        ax.set_xlim(intorno_min - 0.6, intorno_max + 0.6)
        ax.set_ylim(-1, 2.6)
        ax.get_yaxis().set_visible(False)
        ax.set_aspect('equal')
        
        ax.set_xticks([x_target])
        ax.tick_params(axis='x', labelsize=7)

    # Nascondiamo eventuali celle vuote se la griglia in eccesso
    for j in range(num_collisioni, len(assi_piatti)):
        assi_piatti[j].set_visible(False)

    plt.suptitle(f'Intersezioni Geometriche X e Pendenze K (Modulo 6) alla Quota H={H}\n[AZZURRO = K Primo (Miller-Rabin) | GIALLO = K Composto]', fontsize=9, y=0.98)
    plt.show()

def main():
    print("=== SCANNER GEOMETRICO MODULO 6 (CLI Mode) ===")
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
                
            scansiona_e_genera_intorni_led(H_scelta)
        except ValueError:
            print("[ERRORE] Inserisci un numero intero valido.")
        except KeyboardInterrupt:
            print("\nUscita dal programma.")
            break

if __name__ == "__main__":
    main()

import math
import tkinter as tk
from tkinter import simpledialog
import matplotlib.pyplot as plt
import numpy as np
import warnings
import logging

warnings.filterwarnings("ignore")
logging.getLogger('matplotlib').setLevel(logging.ERROR)

def miller_rabin(n, k=5):
    """Test di primalità di Miller-Rabin per gestire in sicurezza anche numeri grandi."""
    if n < 2: return False
    if n in (2, 3): return True
    if n % 2 == 0: return False
    
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
        
    for _ in range(k):
        a = np.random.randint(2, n - 1)
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
    colore_pixel = {}
    
    print(f"\n--- SCANSIONE GEOMETRICA MODULO 6 & INTERSEZIONI (Quota H = {H}, M = {M}) ---")
    
    # Cerchiamo le intersezioni geometriche X e le pendenze k associate
    # Ricaviamo i divisori d di M tramite le coordinate X: denominatore = 2*X + 1
    for i in range(1, int(math.sqrt(M)) + 1, 2):
        if M % i == 0:
            divisori = [i, M // i]
            for denominatore in divisori:
                # Verifichiamo il vincolo geometrico del Modulo 6 (resto 1 o 5)ma aggiungiamo anche il 3 per non perderlo come divisore
                
                resto = denominatore % 6
                if resto == 1 or resto == 5 or denominatore == 3 or denominatore == 1:
                    # Troviamo l'intersezione intera X geometrica
                    x = (denominatore - 1) // 2
                    # Calcoliamo la pendenza / co-fattore k corrispondente
                    k = M // denominatore
                    
                    if k > 0:
                        es_primo = miller_rabin(k)
                        tipo_resto = "+1" if resto == 1 else ("+5" if resto == 5 else "base")
                        colore_pixel[x] = (k, es_primo, tipo_resto)
                        print(f"[INTERSEZIONE X={x}] Divisore={denominatore} (Mod 6: {resto}) -> Pendenza k = {k} (Primo: {es_primo})")

    if not colore_pixel: 
        print("Nessuna intersezione geometrica valida trovata per questa quota.")
        return

    coordinate_attive = sorted(list(colore_pixel.keys()))
    num_collisioni = len(coordinate_attive)

    # --- GENERATORE DI MATRICE GRAFICA MULTI-PANNELLO ---
    fig, assi = plt.subplots(1, num_collisioni, squeeze=False, figsize=(3.5 * num_collisioni, 3))
    fig.subplots_adjust(wspace=0.4)

    for idx, x_target in enumerate(coordinate_attive):
        ax = assi[0, idx]
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
                
                testo_k = f"{k}" if k < 1000000 else f"{k:.4e}"
                ax.text(x_target, 0.55, f'X={x_target}\nk={testo_k} (M6:{tipo_resto})', ha='center', va='bottom', 
                       fontsize=7, fontweight='bold', color='black',
                       bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.85), zorder=3)
            else:
                rect = plt.Rectangle((x_intorno - 0.4, -0.4), 0.8, 0.8, facecolor='black', edgecolor='#333333', linewidth=0.5, zorder=1)
                ax.add_patch(rect)

        ax.set_xlim(intorno_min - 0.6, intorno_max + 0.6)
        ax.set_ylim(-1, 2.2)
        ax.get_yaxis().set_visible(False)
        ax.set_aspect('equal')
        
        ax.set_xticks([x_target])
        ax.tick_params(axis='x', labelsize=8)

    plt.suptitle(f'Intersezioni Geometriche X e Pendenze K (Modulo 6) alla Quota H={H}\n[AZZURRO = K Primo (Miller-Rabin) | GIALLO = K Composto]', fontsize=9, y=0.98)
    plt.show()

def main():
    root = tk.Tk()
    root.withdraw()
    while True:
        input_utente = simpledialog.askstring("Scanner Geometrico Intersezioni X", "Inserisci la quota H:")
        if input_utente is None or input_utente.strip().lower() == 'esci': break
        try:
            H_scelta = int(input_utente.strip())
            if H_scelta < 0: continue
            scansiona_e_genera_intorni_led(H_scelta)
        except ValueError: pass
    root.destroy()

if __name__ == "__main__":
    main()

import math
import tkinter as tk
from tkinter import simpledialog
import matplotlib.pyplot as plt
import numpy as np
import warnings
import logging

warnings.filterwarnings("ignore")
logging.getLogger('matplotlib').setLevel(logging.ERROR)

def is_prime(n):
    """Determina se la pendenza k è un numero primo."""
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

def scansiona_e_genera_intorni_led(H):
    M = 2 * H + 1
    colori_pixel = {}
    
    print(f"\n--- AVVIO SCANSIONE HARDWARE AD ALTA PRECISIONE (Quota H = {H}) ---")
    
    # 1. Calcolo istantaneo di tutte le collisioni reali tramite divisori
    for i in range(1, int(math.sqrt(M)) + 1, 2):
        if M % i == 0:
            # Primo divisore (sotto la radice)
            denominatore1 = i
            x1 = (denominatore1 - 1) // 2
            k1 = M // denominatore1
            if k1 > 0:
                colori_pixel[x1] = (k1, is_prime(k1))
                print(f"[HIT] Rilevato pixel a X = {x1} | k = {k1}")
            
            # Secondo divisore complementare (sopra la radice)
            denominatore2 = M // i
            x2 = (denominatore2 - 1) // 2
            k2 = M // denominatore2
            if k2 > 0:
                colori_pixel[x2] = (k2, is_prime(k2))
                print(f"[HIT] Rilevato pixel a X = {x2} | k = {k2}")

    if not colori_pixel: 
        print("Nessuna collisione trovata.")
        return

    coordinate_attive = sorted(list(colori_pixel.keys()))
    num_collisioni = len(coordinate_attive)

    # --- GENERATORE DI MATRICE GRAFICA MULTI-PANNELLO (FOCALIZZATO SUGLI INTORNI) ---
    # Creiamo un sub-plot per ogni collisione trovata, disposti in riga
    fig, assi = plt.subplots(1, num_collisioni, squeeze=False, figsize=(3.5 * num_collisioni, 3))
    fig.subplots_adjust(wspace=0.4)

    for idx, x_target in enumerate(coordinate_attive):
        ax = assi[0, idx]
        k, es_primo = colori_pixel[x_target]
        colore_led = '#00E5FF' if es_primo else '#FFEA00' # Azzurro o Giallo
        
        # Definiamo un intorno strettissimo di 3 pixel a sinistra e 3 a destra
        intorno_min = x_target - 3
        intorno_max = x_target + 3
        
        # Disegnamo lo sfondo nero solo per questo intorno spaziale
        sfondo = plt.Rectangle((intorno_min - 0.5, -0.4), 7, 0.8, facecolor='black', edgecolor='none', zorder=1)
        ax.add_patch(sfondo)
        
        # Disegnamo i pixel spenti dell'intorno come piccoli quadrati vuoti
        for x_intorno in range(intorno_min, intorno_max + 1):
            if x_intorno == x_target:
                # Questo è il pixel di collisione: accendiamo il LED luminoso
                rect = plt.Rectangle((x_intorno - 0.4, -0.4), 0.8, 0.8, facecolor=colore_led, edgecolor='white', linewidth=1.5, zorder=2)
                ax.add_patch(rect)
                
                # Formattazione del testo per evitare stringhe chilometriche se k è enorme
                testo_k = f"{k}" if k < 1000000 else f"{k:.4e}"
                ax.text(x_target, 0.55, f'X={x_target}\nk={testo_k}', ha='center', va='bottom', 
                         fontsize=8, fontweight='bold', color='black',
                         bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.85), zorder=3)
            else:
                # Pixel spenti vicini
                rect = plt.Rectangle((x_intorno - 0.4, -0.4), 0.8, 0.8, facecolor='black', edgecolor='#333333', linewidth=0.5, zorder=1)
                ax.add_patch(rect)

        # Regolazioni estetiche del singolo intorno
        ax.set_xlim(intorno_min - 0.6, intorno_max + 0.6)
        ax.set_ylim(-1, 2.2)
        ax.get_yaxis().set_visible(False)
        ax.set_aspect('equal')
        
        # Mostriamo sull'asse solo la coordinata esatta del punto d'impatto
        ax.set_xticks([x_target])
        ax.tick_params(axis='x', labelsize=8)

    plt.suptitle(f'Mappatura Digitale degli Intorni di Collisione alla Quota H\n[AZZURRO = K Primo | GIALLO = K Composto]', fontsize=10, y=0.98)
    plt.show()

def main():
    root = tk.Tk()
    root.withdraw()
    while True:
        input_utente = simpledialog.askstring("Hardware Scanner", "Inserisci la quota H (anche numeri astronomici):")
        if input_utente is None or input_utente.strip().lower() == 'esci': break
        try:
            H_scelta = int(input_utente.strip())
            if H_scelta < 0: continue
            scansiona_e_genera_intorni_led(H_scelta)
        except ValueError: pass
    root.destroy()

if __name__ == "__main__":
    main()

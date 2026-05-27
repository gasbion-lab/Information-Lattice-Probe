import math
import time
from numba import njit

@njit(fastmath=True)
def ciclo_scansione_numba_allineato(N, d_allineato, passo, max_passi):
    """Ciclo geometrico ultra-veloce in codice macchina nativo.
    Grazie all'allineamento dell'offset, d avanza a colpi sicuri sul reticolo."""
    d_tentativo = d_allineato
    
    for _ in range(max_passi):
        m_quadrato = N + (d_tentativo * d_tentativo)
        
        # Radice hardware CPU ottimizzata da Numba
        m = int(math.sqrt(m_quadrato))
        
        if m * m == m_quadrato:
            return d_tentativo, m
            
        d_tentativo += passo
    return -1, -1

def fattorizzazione_geometrica_mac_allineato(N):
    if N <= 1 or N % 2 == 0:
        return None, "Inserisci un numero dispari maggiore di 1."
    
    # === SISTEMA 1: GRIGLIA A PASSO 6 ===
    Y = (N - 1) // 2
    rette_partenza = [5, 6, 8, 9]
    x_passo6 = None
    y0_valida = None
    
    for y0 in rette_partenza:
        if (Y - y0) % 6 == 0:
            x_passo6 = (Y - y0) // 6
            y0_valida = y0
            break
            
    if x_passo6 is None:
        return None, "Il numero non rientra nella griglia standard a passo 6."

    print(f"\n🎯 [INTERSEZIONE INTERA TROVATA]:")
    print(f"   • Retta madre con valore intero (y0): {y0_valida}")
    print(f"   • Valore della coordinata lineare (x): {x_passo6}")
    print(f"   --------------------------------------------------------")

    # === SISTEMA 2: STRATEGIA DECRESCENTE CON CORREZIONE OFFSET ===
    passo_secondario = 45 if y0_valida in [8, 9] else 30
    passi_da_eseguire = [90, passo_secondario, 6]
    
    # Base residua del passo 6
    if y0_valida == 6: d_base_6 = 0
    elif y0_valida == 8: d_base_6 = 2
    elif y0_valida == 9: d_base_6 = 3
    elif y0_valida == 5: d_partenza_base = 1 # Corretto refuso firma

    max_passi = 50000000 

    for passo_attuale in passi_da_eseguire:
        print(f"   🚀 Avvio scansione Numba con **Passo {passo_attuale}**...")
        
        # --- CALCOLO MATEMATICO DELL'OFFSET DI PARTENZA ---
        # Sincronizziamo il punto di partenza affinché rispetti sia la retta mod 6
        # sia la griglia del passo macro (90, 45, 30), eliminando l'offset error.
        d_allineato = d_base_6
        while d_allineato % passo_attuale != d_base_6 % passo_attuale:
            # Se stiamo testando passi superiori a 6, cerchiamo il primo nodo coerente
            if passo_attuale == 6:
                break
            # Algoritmo di allineamento della griglia modulare
            # Verifica se l'estensione genera un residuo quadratico valido
            if (N + d_allineato**2) % passo_attuale == (N + d_base_6**2) % passo_attuale:
                break
            d_allineato += 6
            
        # 📋 Mostriamo i primi 3 valori reali sincronizzati che verranno testati
        print(f"     📋 [Primi valori calibrati per Passo {passo_attuale}]:")
        for i in range(3):
            d_test = d_allineato + (i * passo_attuale)
            print(f"       -> Test {i+1}: d = {d_test}  =>  m^2 = {N + d_test*d_test}")
        print(f"     --------------------------------------------------------")
        
        # Esecuzione del ciclo JIT sulla CPU del Mac
        d_trovato, m_trovato = ciclo_scansione_numba_allineato(N, d_allineato, passo_attuale, max_passi)
        
        if d_trovato != -1:
            p = m_trovato - d_trovato
            q = m_trovato + d_trovato
            
            if p > 1 and p * q == N:
                x_fascio_p = (N - p) // (2 * p)
                x_fascio_q = (N - q) // (2 * q)
                return {
                    "N": N, "Y": Y, "y0": y0_valida, "x_passo6": x_passo6,
                    "p": p, "q": q, "d": d_trovato, "m": m_trovato,
                    "x_fascio_p": x_fascio_p, "x_fascio_q": x_fascio_q,
                    "passo_usato": passo_attuale
                }, None
                
        print(f"   ⚠️ Griglia del Passo {passo_attuale} superata senza convergenza.\n")

    return None, "Fattorizzazione non riuscita: la semidifferenza esce dai limiti calibrati."

# --- INTERFACCIA PER IL MAC ---
print("==========================================================")
print("  Motore Geometrico Allineato Numba (Specifico per Mac)   ")
print("==========================================================")

while True:
    input_utente = input("Inserisci il numero da analizzare (o 'esci'): ").strip()
    if input_utente.lower() == 'esci':
        print("\nProgramma terminato. Grazie!")
        break
    if not input_utente.isdigit():
        print("❌ Inserisci un numero intero valido.\n")
        continue
        
    numero = int(input_utente)
    
    tempo_inizio = time.perf_counter()
    risultato, errore = fattorizzazione_geometrica_mac_allineato(numero)
    tempo_fine = time.perf_counter()
    
    if errore:
        print(f"❌ {errore}\n")
    else:
        print(f"\n✅ RISULTATO COMPLETO:")
        print(f"  • Risolto con successo usando il **Passo {risultato['passo_usato']}**")
        print(f"  --------------------------------------------------------")
        print(f"  • Punti interi di intersezione del fascio rilevati a:")
        print(f"     - x_p = {risultato['x_fascio_p']} (per la retta k = p = {risultato['p']})")
        print(f"     - x_q = {risultato['x_fascio_q']} (per la retta k = q = {risultato['q']})")
        print(f"  --------------------------------------------------------")
        print(f"  🔑 FATTORI ESTRATTI: {risultato['p']} e {risultato['q']} (Distanza d = {risultato['d']})")
        print(f"  ⏱️ Tempo totale di calcolo CPU (Mac + Numba): {tempo_fine - tempo_inizio:.6f} secondi")
        print("==================================================\n")

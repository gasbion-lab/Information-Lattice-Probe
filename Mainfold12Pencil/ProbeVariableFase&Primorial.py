import math
import random
import time

def miller_rabin(n, k=50): # Massima precisione per il test di laboratorio
    if n <= 1: return False
    if n <= 3: return True
    if n % 2 == 0 or n % 3 == 0 or n % 5 == 0: return False
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

def drilling_resonance_350():
    # --- CONFIGURAZIONE CON INPUT UTENTE ---
    print("\n--- INSERIMENTO PARAMETRI DI PERFORAZIONE ---")
    try:
        EXP = int(input("Inserisci l'esponente (es. 500): "))
        FASE_TARGET = float(input("Inserisci la FASE TARGET (es. -0.9818): "))
        TOLLERANZA = float(input("Inserisci la TOLLERANZA (es. 0.0005): "))
        RANGE_SCANSIONE = int(input("Inserisci il RANGE DI SCANSIONE (es. 5000000): "))
    except ValueError:
        print("Errore: Inserire valori numerici validi.")
        return
    
    print("\n" + "█"*60)
    print(f"    --- PERFORAZIONE COERENTE: RISONANZA {FASE_TARGET} ---")
    print(f"    --- ANALISI SU {RANGE_SCANSIONE} PASSI A 10^{EXP} ---")
    print("█"*60)
    
    n_base = 10**EXP
    p_inizio = n_base + (11 - (n_base % 180)) % 180
    
    # 1. Fase di selezione (istantanea)
    print(f"\n[1/2] Selezione target in fase...")
    targets = []
    for i in range(RANGE_SCANSIONE):
        # Calcoliamo la fase per ogni passo
        fase = math.asin(math.sin(i / 100 + EXP))
        if abs(fase - FASE_TARGET) < TOLLERANZA:
            targets.append((i, fase))
    
    num_targets = len(targets)
    if num_targets == 0:
        print("Nessun punto trovato con questa tolleranza. Prova ad aumentarla.")
        return

    print(f"Trovati {num_targets} punti di risonanza su {RANGE_SCANSIONE} passi.")
    print(f"Risparmio di calcolo: {((1 - num_targets/RANGE_SCANSIONE)*100):.2f}%")
    
    # 2. Fase di caccia (Miller-Rabin selettivo)
    print(f"\n[2/2] Inizio perforazione dei punti selezionati...\n")
    start_time = time.perf_counter()
    trovati = 0

    try:
        for idx, (step, fase_effettiva) in enumerate(targets):
            p = p_inizio + (step * 510510)
            
            # TEST INDIPENDENTE SULLE DUE POSSIBILI COPPIE DEL MANIFOLD
            is_p1 = miller_rabin(p)
            is_p3 = miller_rabin(p+2)
            
            is_p7 = miller_rabin(p+6)
            is_p9 = miller_rabin(p+8)
            
            # Verifichiamo se c'è ALMENO una coppia gemella (1-3 OPPURE 7-9)
            found_1_3 = is_p1 and is_p3
            found_7_9 = is_p7 and is_p9
            
            if found_1_3 or found_7_9:
                trovati += 1
                res = [is_p1, is_p3, is_p7, is_p9]
                hits = sum(res)
                
                if hits == 4:
                    tipo = "!!! QUADRUPLA !!!"
                elif hits == 3:
                    tipo = "TRIPLETTA"
                else:
                    # Specifichiamo quale coppia abbiamo trovato
                    tipo = "COPPIA (1-3)" if found_1_3 else "COPPIA (7-9)"
                    if found_1_3 and found_7_9: tipo = "DOPPIA COPPIA" # Molto raro

                print(f"\n[RISONANZA COLPITA] {tipo}")
                print(f"PASSO: {step} | FASE: {fase_effettiva:+.5f}")
                print(f"P_base: {p} | Struttura: {res}")
                print("-" * 40)


            
            if (idx + 1) % 500 == 0:
                elapsed = time.perf_counter() - start_time
                print(f"Analizzati: {idx+1}/{num_targets} | Tempo: {elapsed:.1f}s | Trovati: {trovati}")

    except KeyboardInterrupt:
        print("\nPerforazione interrotta.")

    print(f"\nFine missione. Punti di risonanza analizzati: {num_targets}")
    print(f"Target speciali scovati sulla frequenza {FASE_TARGET}: {trovati}")

if __name__ == "__main__":
    drilling_resonance_350()

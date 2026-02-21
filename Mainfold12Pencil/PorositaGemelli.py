import math
while True:
 def is_prime(n):
    if n < 2: return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0: return False
    return True

 def analizza_rapporto_gemelli(start_p, window_size, n_moduli=10000):
    # Generiamo i moduli k del Pencil (primi >= 5, escludendo il 2 e 3 del modulo 12)
    moduli_k = []
    p = 5
    while len(moduli_k) < n_moduli:
        if is_prime(p):
            moduli_k.append(p)
        p += 2

    # Setaccio delle posizioni P nella finestra scelta
    # Usiamo un array di booleani: True = Libero (Vuoto), False = Colpito (Composto)
    setaccio = [True] * window_size
    
    for k in moduli_k:
        fase = (k - 1) // 2
        # Il primo colpo del modulo k è a P = k + fase (x=1)
        # Calcoliamo il primo salto utile all'interno della nostra finestra
        primo_salto = k + fase
        
        # Se la finestra parte molto avanti, saltiamo i passi inutili
        if primo_salto < start_p:
            start_offset = (start_p - primo_salto + k - 1) // k
            corrente = primo_salto + start_offset * k
        else:
            corrente = primo_salto
            
        while corrente < start_p + window_size:
            setaccio[corrente - start_p] = False
            corrente += k

    # Conteggio Vuoti e Gemelli
    vuoti_totali = 0
    coppie_gemelle = 0
    
    # Scorriamo il setaccio a passi di 6 (il ciclo del Manifold 12)
    # Cerchiamo i vuoti nelle posizioni relative 2 e 3 di ogni ciclo
    for i in range(0, window_size - 6, 6):
        p5_index = i + 2
        p7_index = i + 3
        
        if p5_index < window_size and setaccio[p5_index]:
            vuoti_totali += 1
        if p7_index < window_size and setaccio[p7_index]:
            vuoti_totali += 1
            
        # Verifica se formano una coppia gemella (entrambi vuoti)
        if p5_index < window_size and p7_index < window_size:
            if setaccio[p5_index] and setaccio[p7_index]:
                coppie_gemelle += 1

    porosita = (vuoti_totali / (window_size / 3)) * 100 # Rispetto ai candidati totali
    rapporto_gemelli = (coppie_gemelle * 2 / vuoti_totali) * 100 if vuoti_totali > 0 else 0

    print(f"Analisi Finestra: P=[{start_p} - {start_p + window_size}]")
    print(f"Porosità Totale: {porosita:.2f}%")
    print(f"Vuoti che appartengono a una coppia gemella: {rapporto_gemelli:.2f}%")
    print(f"Coppie Gemelle trovate: {coppie_gemelle}")
    print("-" * 30)

# Confronto tra due finestre distanti
 analizza_rapporto_gemelli(0, 20000)
 analizza_rapporto_gemelli(10**100, 20000)
 break

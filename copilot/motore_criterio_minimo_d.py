import math
import time

def calcola_fattori_fermat_preciso(m, N):
    """Metodo di Fermat puro: trova m tale che m² - N sia un quadrato perfetto."""
    d2 = (m * m) - N
    if d2 < 0:
        return None
    
    d = math.isqrt(d2)
    if d * d == d2:
        p = m - d
        q = m + d
        return p, q, m, d
    return None

def motore_fisarmonica_criterio_minimo_d_v2(N, PASSO_MACRO=None, verbose=True):
    """
    Algoritmo di fattorizzazione con fisarmonica basato su:
    
    CRITERIO: Monitoriamo d_approx = ⌊√(m²-N)⌋ e rilevi il MINIMO LOCALE
    """
    
    m0 = math.isqrt(N) + 1
    
    if PASSO_MACRO is None:
        PASSO_MACRO = max(100, int(math.sqrt(N) * 0.00001))
    
    if verbose:
        print("\n" + "="*75)
        print("   MOTORE FISARMONICA: CRITERIO MINIMO DI D (V2)")
        print("="*75)
        print(f"• Semiprimo N              : {N}")
        print(f"• Partenza da m0           : {m0}")
        print(f"• Passo Macro              : {PASSO_MACRO}")
        print("-----------------------------------------------------------------------\n")
    
    # ==================================================================
    # FASE 1: CORSA IN AVANTI FINO A RILEVARE IL MINIMO DI d_approx
    # ==================================================================
    if verbose:
        print("-> FASE 1: Ricerca del minimo di d_approx...")
    
    m = m0
    d_approx_prec = math.isqrt((m * m) - N)
    passi = 0
    m_minimo = m0
    d_approx_minimo = d_approx_prec
    minimo_trovato = False
    
    while passi < 10**8:
        m += PASSO_MACRO
        passi += 1
        
        # Verifica se è la soluzione
        risultato = calcola_fattori_fermat_preciso(m, N)
        if risultato:
            p, q, m_sol, d_sol = risultato
            if verbose:
                print(f"\n💥 [SOLUZIONE TROVATA NELLA FASE 1]")
            return p, q, m_sol, d_sol
        
        # Calcola d_approx
        d2 = (m * m) - N
        d_approx = math.isqrt(d2)
        
        # Monitoraggio periodico
        if verbose and passi % max(1, 10**8 // 100) == 0:
            print(f"[PASSO #{passi:>10}] m = {m:>20} | d_approx = {d_approx:>20}")
        
        # CRITERIO: d_approx raggiunge un minimo e poi ricomincia a crescere
        if d_approx > d_approx_prec and d_approx_prec < d_approx_minimo * 1.01:
            # La velocità di crescita è aumentata e d era vicino al minimo
            m_minimo = m - PASSO_MACRO
            d_approx_minimo = d_approx_prec
            minimo_trovato = True
            if verbose:
                print(f"\n💡 [MINIMO DI d_approx RILEVATO al Passo #{passi}]")
                print(f"   -> m = {m_minimo}")
                print(f"   -> d_approx_minimo = {d_approx_minimo}")
            break
        
        # Traccia il minimo assoluto
        if d_approx < d_approx_minimo:
            d_approx_minimo = d_approx
            m_minimo = m
        
        d_approx_prec = d_approx
    
    if not minimo_trovato:
        if verbose:
            print(f"\n⚠️  Minimo non trovato, uso il minimo tracciato")
        m_minimo_search = m_minimo
    else:
        m_minimo_search = m_minimo
    
    # ==================================================================
    # FASE 2: FISARMONICA ATTORNO AL MINIMO
    # ==================================================================
    if verbose:
        print(f"\n-> FASE 2: Fisarmonica attorno a m={m_minimo_search}...")
    
    passo = max(PASSO_MACRO // 10, 1)
    m = m_minimo_search - PASSO_MACRO
    
    # Protezione: assicurati che m² - N sia non negativo
    if m < m0:
        m = m0
    
    direzione = 1
    flessi = 0
    max_flessi = 30
    
    # Calcola d_approx iniziale con protezione
    d2_start = (m * m) - N
    if d2_start < 0:
        d_approx_prec = 0
    else:
        d_approx_prec = math.isqrt(d2_start)
    
    while flessi < max_flessi and passo >= 1:
        m_nuovo = m + direzione * passo
        
        # Protezione: non andare sotto m0
        if m_nuovo < m0:
            passo = max(1, passo // 10)
            continue
        
        m = m_nuovo
        
        # Verifica se è la soluzione
        risultato = calcola_fattori_fermat_preciso(m, N)
        if risultato:
            p, q, m_sol, d_sol = risultato
            if verbose:
                print(f"\n   💥 [SOLUZIONE TROVATA DURANTE FISARMONICA]")
            return p, q, m_sol, d_sol
        
        # Calcola d_approx
        d2 = (m * m) - N
        if d2 < 0:
            d_approx = 0
        else:
            d_approx = math.isqrt(d2)
        
        # Se d_approx si è incrementato dopo aver diminuito, inverti marcia
        if d_approx > d_approx_prec:
            direzione *= -1
            passo = max(1, passo // 10)
            flessi += 1
            if verbose and flessi <= 10:
                print(f"   → Flesso #{flessi}: inversione a m={m}, d_approx={d_approx}, passo={passo}")
        
        d_approx_prec = d_approx
    
    # ==================================================================
    # FASE 3: RICERCA LINEARE FINE
    # ==================================================================
    if verbose:
        print(f"\n-> FASE 3: Ricerca lineare fino a soluzione...")
    
    search_range = max(100000, PASSO_MACRO * 100)
    m_start = max(m0, m - search_range)
    m_end = m + search_range
    
    for m_test in range(m_start, m_end + 1):
        risultato = calcola_fattori_fermat_preciso(m_test, N)
        if risultato:
            p, q, m_sol, d_sol = risultato
            if verbose:
                print(f"   💥 [SOLUZIONE TROVATA NELLA FASE 3]")
            return p, q, m_sol, d_sol
    
    if verbose:
        print(f"\n❌ Soluzione non trovata")
    
    return None

if __name__ == "__main__":
    test_cases = [
        15,                              # 3 × 5
        91,                              # 7 × 13
        2021,                            # 43 × 47
        162373,                          # Test case
        208701896930419739418841,        # Il numero grande
    ]
    
    for N in test_cases:
        print(f"\n\n{'#'*75}")
        print(f"TEST: N = {N}")
        print(f"{'#'*75}")
        
        t_start = time.perf_counter()
        risultato = motore_fisarmonica_criterio_minimo_d_v2(N, verbose=True)
        t_end = time.perf_counter()
        
        if risultato:
            p, q, m_f, d_f = risultato
            print("\n" + "="*75)
            print("   🎯🎯 FATTORIZZAZIONE COMPLETATA! 🎯🎯")
            print("="*75)
            print(f"• Fattore p                : {p}")
            print(f"• Fattore q                : {q}")
            print(f"• Asse m Risolutivo        : {m_f}")
            print(f"• Distanza d Reale         : {d_f}")
            print(f"• Verifica p × q = N       : {p * q == N} ✓")
            print(f"• Tempo di elaborazione    : {(t_end - t_start):.4f} secondi")
            print("="*75)
        else:
            print(f"\n❌ Fattorizzazione fallita per N={N}")

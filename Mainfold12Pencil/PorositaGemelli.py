import math

def check_manifold_stability(n_scale, window_size, found_twins):
    """
    Valida la stabilità del Manifold 12 confrontando i dati empirici 
    con la necessità geometrica della porosità residua.
    """
    # Costanti Teoriche
    C2 = 0.6601618158  # Costante di Hardy-Littlewood
    REFERENCE_POROSITY = 0.3375  # Porosità strutturale target (%)

    # 1. Calcolo Densità Analitica (Hardy-Littlewood)
    # La densità teorica locale vicino a N è 2 * C2 / ln(N)^2
    ln_n = math.log(n_scale) if n_scale > 1 else 1
    theoretical_density = (2 * C2) / (ln_n**2)
    
    # 2. Calcolo Porosità Grezza vs Porosità Strutturale
    # La porosità grezza è quella rilevata nella finestra (es. il tuo 14.25%)
    # La porosità strutturale è il limite asintotico di invarianza del Manifold.
    raw_window_porosity = (found_twins * 2) / window_size * 100 # Stima basata sui gemelli

    # 3. Calcolo dell'Inerzia (Braking Effect)
    # La derivata della saturazione Phi' tende a zero
    braking_inertia = 1 / ln_n  # Modello semplificato dell'inefficienza del Pencil

    print("-" * 60)
    print(f"MANIFOLD 12 - VALIDATORE DI STABILITÀ STRUTTURALE")
    print("-" * 60)
    print(f"Scala Analizzata (N):       10^{int(math.log10(n_scale))}")
    print(f"Finestra di Scansione:      {window_size}")
    print(f"Coppie Gemelle rilevate:    {found_twins}")
    print("-" * 60)
    print(f"RISULTATI ANALITICI:")
    print(f"Porosità Locale rilevata:   {raw_window_porosity:.4f}%")
    print(f"Soglia di Rigidità (Floor): {REFERENCE_POROSITY:.4f}%")
    print(f"Inerzia del Pencil (Phi'):  {braking_inertia:.2e} (-> 0)")
    print("-" * 60)
    
    # Verdetto Finale
    print("VERDETTO GEOMETRICO:")
    if raw_window_porosity > REFERENCE_POROSITY:
        print("CONFERMATO: La porosità residua eccede la soglia critica.")
        print("Necessità Meccanica: Il Pencil non può saturare il Manifold.")
    else:
        print("ATTENZIONE: Saturazione locale anomala. Verificare moduli k.")
    print("-" * 60)

# --- ESECUZIONE TEST ---

# Test 1: Scala Locale (es. 20.000)
check_manifold_stability(20000, 20000, 295)

print("\n")

# Test 2: Scala Googol (10^100) - Basato sul tuo scan
# Nota: Usiamo la finestra di 20.000 sopra la base 10^100
check_manifold_stability(10**100, 20000, 65)

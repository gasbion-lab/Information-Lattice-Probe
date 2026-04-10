import matplotlib.pyplot as plt
import numpy as np
import textwrap
import sympy
import matplotlib
# Developed by Gasbion-lab | Part of the Information Lattice Field Theory (ILFT)
# Backend per stabilità su macOS
matplotlib.use('TkAgg') 

def format_long_number(n, width=40):
    return "\n".join(textwrap.wrap(str(n), width))

# --- 1. INPUT E AUTO-ALLINEAMENTO RIGOROSO ---
print("-" * 60)
print("GASBION PROBE v4.4 | AUTO-ALIGNMENT N ≡ 11 (mod 12)")
print("-" * 60)
val_in = input("GASBION > Inserisci N di partenza (qualsiasi scala): ").strip().replace("^", "**")
mult_in = input("GASBION > Moltiplicatore Passo (Default 1 = 180u): ").strip()

try:
    N_TARGET = int(eval(val_in))
    
    # Correzione: Riportiamo N a congruenza 11 modulo 12
    # Se inserisci 10**301+1 e finisce a 19, il codice sottrae lo scostamento
    # per tornare alla posizione '11' più vicina.
    resto = N_TARGET % 12
    diff = (resto - 11) % 12
    N_START = N_TARGET - diff
    
    # Se il numero è pari o finisce per 5 dopo la correzione, assicuriamo sia dispari
    if N_START % 2 == 0: N_START -= 1 
    
    MOLT = int(mult_in) if mult_in else 1
except Exception as e:
    print(f"Errore input: {e}. Uso default N=11")
    N_START = 11; MOLT = 1

STEP_N = 180 * MOLT
ROWS, COLS = 200, 200
N_TOTAL = ROWS * COLS
N_END = N_START + (N_TOTAL * STEP_N)

# --- 2. MOTORE DI CALCOLO ---
print(f"\n[CALCOLO] Analisi avviata da N={N_START}")
print(f"Punto di partenza allineato a modulo 12: {N_START % 12}")
red, cyan, green, white = [], [], [], []

for i in range(N_TOTAL):
    n = N_START + (i * STEP_N)
    # Test Pattern Quadrupla: [n, n+2, n+6, n+8]
    # Questo pattern richiede l'allineamento a 11 per non colpire multipli di 3 e 5
    p = [sympy.isprime(n + d) for d in [0, 2, 6, 8]]
    
    if all(p):
        white.append(i) # QUADRUPLA (BIANCO)
    elif (p[0] and p[1]) or (p[2] and p[3]):
        green.append(i) # GEMELLI (FUCSIA)
    elif any(p):
        cyan.append(i)  # PRIMO ISOLATO (CIANO)
    else:
        red.append(i)   # COMPOSTO (ROSSO)

# --- 3. RENDERING GRAFICO ---
fig, ax = plt.subplots(figsize=(18, 10), facecolor='black')
plt.subplots_adjust(left=0.38, right=0.98)

x, y = np.meshgrid(np.arange(COLS), np.arange(ROWS))
x_f, y_f = x.flatten(), y[::-1].flatten()

colors = np.full((N_TOTAL, 3), 0.02)
if red: colors[red] = [0.85, 0.0, 0.0]     # Rosso (Pencil Hit)
if cyan: colors[cyan] = [0.0, 1.0, 1.0]   # Ciano (Single)
if green: colors[green] = [1.0, 0.0, 1.0] # Fucsia (Twin)
if white: colors[white] = [1.0, 1.0, 1.0] # Bianco (Quadruple)

ax.scatter(x_f, y_f, s=25, c=colors, marker='s', edgecolors='none')
ax.set_facecolor('black')
ax.set_axis_off()

# BOX DATI LOG
info_str = "RESONANCE RADAR DATA LOG v4.4\n" + "="*40 + "\n\n"
info_str += "STARTING NODE (Corrected to 11):\n" + format_long_number(N_START) + "\n\n"
info_str += "ENDING NODE (19-Range):\n" + format_long_number(N_END + 8) + "\n\n"
info_str += f"RESONANCE STEP:  {STEP_N} units\n"
info_str += f"TOTAL NODES:     {N_TOTAL}\n\n"
info_str += f"SINGLE PRIMES:   {len(cyan)} (CIANO)\n"
info_str += f"TWIN PAIRS:      {len(green)} (FUCSIA)\n"
info_str += f"QUADRUPLETS:     {len(white)} (WHITE)\n\n"
info_str += "="*40 + "\n"
info_str += "LOGIC: Auto-aligned to N ≡ 11 (mod 12)\n"
info_str += "PATTERN: [n, n+2, n+6, n+8]"

fig.text(0.02, 0.5, info_str, color='#00FF41', fontsize=10, family='monospace', 
         va='center', bbox=dict(facecolor='black', edgecolor='#00FF41', lw=2, pad=10))

print("\n[OK] Analisi completata. Visualizzazione radar in corso...")
plt.show()

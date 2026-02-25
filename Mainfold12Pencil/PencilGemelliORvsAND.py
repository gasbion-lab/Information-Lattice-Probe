import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes, mark_inset

# 1. Data Configuration (Manifold 12 - Binary B)
x_log = np.array([6, 10, 14, 18])
x_val = 10**x_log
c2 = 0.6601618  # Twin Prime Constant

# Mechanical Calculations
manifold = x_val / 45
gemini = 2 * c2 * x_val / (np.log(x_val)**2)
pencil_or = manifold - gemini

# Densities %
dens_gemini = (gemini / manifold) * 100
dens_pencil = (pencil_or / manifold) * 100

# --- CALCOLO RAPPORTI INCREMENTALI (Delta 1 e Delta 2) ---
delta1 = np.zeros(len(dens_gemini))
delta2 = np.zeros(len(dens_gemini))

for i in range(1, len(dens_gemini)):
    delta1[i] = dens_gemini[i] - dens_gemini[i-1]
    if i > 1:
        delta2[i] = delta1[i] - delta1[i-1]

# --- STAMPA A SCHERMO COMPLETA (Dati per Tabella 4) ---
print("\n" + "="*85)
print(f"{'Scale':<10} | {'Twin % (AND)':<15} | {'Obstr % (OR)':<15} | {'Delta 1':<12} | {'Delta 2'}")
print("-" * 85)
for i in range(len(x_log)):
    d1_str = f"{delta1[i]:.4f}" if i > 0 else "---"
    d2_str = f"{delta2[i]:.4f}" if i > 1 else "---"
    print(f"10^{x_log[i]:<7} | {dens_gemini[i]:<15.4f} | {dens_pencil[i]:<15.4f} | {d1_str:<12} | {d2_str}")
print("="*85 + "\n")

# --- GRAFICA (Stile ottimizzato) ---
plt.rcParams.update({'font.size': 11, 'font.family': 'serif'})
fig, ax = plt.subplots(figsize=(12, 7))

# Curve
ax.plot(x_log, dens_pencil, 'o-', label='Pencil Obstruction (OR)', color='gray', alpha=0.6)
ax.plot(x_log, dens_gemini, 's-', label='Twin Density (AND)', color='red', linewidth=2)

# Lente
axins = zoomed_inset_axes(ax, zoom=2.8, loc='center right', borderpad=3) 
axins.plot(x_log, dens_gemini, 's-', color='red', linewidth=2)
axins.set_xlim(13.5, 18.5) 
axins.set_ylim(0.3, 1.3)
axins.grid(True, linestyle=':', alpha=0.5)
mark_inset(ax, axins, loc1=2, loc2=4, fc="none", ec="0.5", linestyle='--')

# Etichette
ax.set_title("Braking Effect Analysis: Limits of Incremental Ratios", fontsize=15, fontweight='bold', pad=20)
ax.set_xlabel("Scale of Analysis (Logarithmic: $10^n$)", fontsize=12)
ax.set_ylabel("Percentage Density (%)", fontsize=12)
ax.legend(loc='upper left', frameon=True, shadow=True)
ax.grid(True, which='both', linestyle='--', alpha=0.4)

# Annotazioni
ax.annotate('Pencil saturation limit → 100%', xy=(18, 99.4), xytext=(11, 92),
             arrowprops=dict(arrowstyle="->", color='black'))
ax.annotate('Braking Effect: Positive Inflection', xy=(17.2, 0.6), xytext=(9.5, 12),
             arrowprops=dict(arrowstyle="->", color='red'), color='red')

fig.subplots_adjust(top=0.9, bottom=0.12, left=0.1, right=0.95)
plt.show()

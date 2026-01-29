import math
import random
import textwrap
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button
from mpmath import mp, riemannr
`# Developed by Gasbion-lab | Part of the Information Lattice Field Theory (ILFT)`
mp.dps = 100 

# --- 1. MOTORE DI CALCOLO: MILLER-RABIN ---
def is_prime_mr(n, k=15):
    if n < 2: return False
    if n == 2 or n == 3: return True
    if n % 2 == 0: return False
    r, d = 0, n - 1
    while d % 2 == 0: r += 1; d //= 2
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1: continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1: break
        else: return False
    return True

# --- 2. INPUT & ANALISI GOLDBACH ---
N_input = input("SISTEMA GASBION > Inserisci N (es. 2**200): ")
N = int(eval(N_input))
if N % 2 != 0: N += 1

print("Sincronizzazione Miller-Rabin & Riemann Density...")
d = 1 if (N//2) % 2 == 0 else 0
while True:
    p1, p2 = (N // 2) - d, (N // 2) + d
    if is_prime_mr(p1) and is_prime_mr(p2): break
    d += 2

rows, cols = 100, 100
n_total = rows * cols
y_start = ((p1 - 1) // 2) - 50

# --- 3. DENSITÀ DI RIEMANN R(x) ---
val_inizio = 2 * y_start + 1
val_fine = 2 * (y_start + n_total) + 1
stima_riemann = float(riemannr(val_fine) - riemannr(val_inizio))

# Pre-calcolo stati e gruppi M12
states = np.zeros(n_total)
gruppi_m12 = {5: [], 7: [], 11: [], 13: []}

for i in range(n_total):
    val = 2 * (y_start + i) + 1
    r12 = val % 12
    r_key = 13 if r12 == 1 else r12
    
    if val == p1 or val == p2:
        states[i] = 2
        if r_key in gruppi_m12: gruppi_m12[r_key].append(i)
    elif is_prime_mr(val):
        states[i] = 1
        if r_key in gruppi_m12: gruppi_m12[r_key].append(i)

reali_trovati = np.sum(states >= 1) # Tutti i verdi + magenta
deviazione = (reali_trovati - stima_riemann) / stima_riemann * 100

# --- 4. SETUP GRAFICO ---
fig = plt.figure(facecolor='black', figsize=(18, 10))
fig.suptitle("GASBION RADAR: MANIFOLD 12 & RIEMANN DENSITY", color='#00FFFF', fontsize=24, fontweight='bold')

ax_lattice = fig.add_axes([0.45, 0.15, 0.5, 0.75], facecolor='black')
ax_lattice.set_xlim(-40, cols + 5)
ax_lattice.set_ylim(-5, rows + 5)
ax_lattice.set_axis_off()

# FOCUS F
ax_lattice.scatter([-35], [rows/2], color='#FF00FF', s=300, marker='*', zorder=10)

def wrap_52(label, value):
    return f"{label}:\n{textwrap.fill(str(value), width=52)}\n\n"

# BOX GASBION INTEGRALE CON RIEMANN
info_str = "GASBION SYSTEM: FOCAL ANALYSIS\n" + "="*48 + "\n"
info_str += "ENGINE: MILLER-RABIN | FOCUS F(-0.5, -0.5)\n"
info_str += "GEN: y = kx + (k-1)/2 | PENCIL PROJECTION\n" + "-"*48 + "\n"
info_str += f"RIEMANN DENSITY R(x) (Sector): {stima_riemann:.2f}\n"
info_str += f"ACTUAL SINGULARITIES FOUND:  {reali_trovati}\n"
info_str += f"STRUCTURAL DEVIATION:     {deviazione:+.4f}%\n" + "-"*48 + "\n"
info_str += wrap_52("GOLDBACH TARGET N ", N)
info_str += wrap_52("p1 (SING.)", p1)
info_str += wrap_52("p2 (SING.)", p2)
info_str += "LINES: M12 Piecewise | RED: Pencil | MAGENTA: Goldbach"

txt_box = fig.text(0.02, 0.5, info_str, color='white', fontsize=8.2, family='monospace', va='center', 
                   bbox=dict(facecolor='#050505', edgecolor='#00FFFF', lw=2))

x_c = [i % cols for i in range(n_total)]
y_c = [rows - 1 - (i // cols) for i in range(n_total)]
scatter = ax_lattice.scatter(x_c, y_c, s=18, color='#151515', zorder=3)

# --- 5. ANIMAZIONE SINCRONIZZATA ---
is_paused = False
pencil_lines = []
spezzate_lines = {5: None, 7: None, 11: None, 13: None}
colors_m12 = {5: '#00FFFF', 7: '#0080FF', 11: '#6600FF', 13: '#00FF00'}

def update(frame):
    if is_paused: return scatter,
    global pencil_lines
    for beam in pencil_lines: beam.remove()
    pencil_lines = []
    
    current_colors = np.full((n_total, 3), 0.1)
    progress = frame * 600
    idx_range = np.arange(n_total)
    
    current_colors[states == 0] = [0.2, 0, 0]
    current_colors[(idx_range < progress) & (states == 0)] = [0.8, 0, 0]
    
    p_v = progress - n_total
    if p_v > 0:
        current_colors[(idx_range < p_v) & (states == 1)] = [0, 1, 0]
        flicker = [1, 0, 1] if frame % 2 == 0 else [0.5, 0, 0.5]
        current_colors[(idx_range < p_v) & (states == 2)] = flicker

        for r, indices in gruppi_m12.items():
            visible_pts = [i for i in indices if i < p_v]
            if len(visible_pts) > 1:
                lx, ly = [x_c[i] for i in visible_pts], [y_c[i] for i in visible_pts]
                if spezzate_lines[r] is None:
                    line, = ax_lattice.plot(lx, ly, color=colors_m12[r], alpha=0.7, lw=1.5, zorder=4)
                    spezzate_lines[r] = line
                else:
                    spezzate_lines[r].set_data(lx, ly)

    if progress < n_total:
        for _ in range(12):
            t_idx = min(progress + random.randint(0, 800), n_total - 1)
            if states[t_idx] == 0:
                l, = ax_lattice.plot([-35, rows/2], [x_c[t_idx], y_c[t_idx]], color='red', alpha=0.3, lw=0.4, zorder=2)
                pencil_lines.append(l)

    scatter.set_facecolors(current_colors)
    return [scatter] + pencil_lines + [l for l in spezzate_lines.values() if l is not None]

def toggle_pause(event):
    global is_paused
    is_paused = not is_paused
    btn_pause.label.set_text('RESUME' if is_paused else 'PAUSE')

ax_pause = plt.axes([0.02, 0.05, 0.1, 0.05])
btn_pause = Button(ax_pause, 'PAUSE', color='#050505', hovercolor='#FF00FF')
btn_pause.label.set_color('white')
btn_pause.on_clicked(toggle_pause)

ani = animation.FuncAnimation(fig, update, frames=n_total//300 + 60, interval=30, blit=False)
plt.show()

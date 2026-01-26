import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button
import numpy as np
import textwrap
from mpmath import mp, riemannr

# Configurazione mpmath per alta precisione
mp.dps = 100 

# --- 1. MOTORE DI CALCOLO (Miller-Rabin) ---
def is_prime(n, k=10):
    if n <= 1: return False
    if n <= 3: return True
    if n % 2 == 0: return False
    r, d = 0, n - 1
    while d % 2 == 0: r += 1; d //= 2
    for _ in range(k):
        a = pow(random.randint(2, n - 2), d, n)
        if a == 1 or a == n - 1: continue
        for _ in range(r - 1):
            a = pow(a, 2, n)
            if a == n - 1: break
        else: return False
    return True

# --- 2. INPUT E RICERCA GOLDBACH ---
import random
print("-" * 50)
N = eval(input("Enter an EVEN number for Goldbach-Riemann: "))
if N % 2 != 0: N += 1

print(f"Probe analytical test in progress...")
found = False
d = 1 if (N//2) % 2 == 0 else 0
while not found:
    p1, p2 = (N // 2) - d, (N // 2) + d
    if is_prime(p1) and is_prime(p2): found = True
    else: d += 2

# Calcolo distanza e stato visibilità
distanza_primi = p2 - p1
fuori_range = distanza_primi > 10000 # 100x100 punti nel lattice

y_start = ((p1 - 1) // 2) - 50
val_inizio = 2 * y_start + 1
val_fine = 2 * (y_start + 10000) + 1

# --- 3. ANALISI SETTORE E RIEMANN R ---
stima_riemann = float(riemannr(val_fine) - riemannr(val_inizio))
densita_teorica_R = stima_riemann / 10000

rows, cols = 100, 100
n_total = rows * cols
red_indices, green_indices, goldbach_indices = [], [], []

for i in range(n_total):
    val = 2 * (y_start + i) + 1
    if val == p1 or val == p2: goldbach_indices.append(i)
    elif is_prime(val): green_indices.append(i)
    else: red_indices.append(i)

densita_reale = len(green_indices) / n_total
deviazione = (densita_reale - densita_teorica_R) / densita_teorica_R * 100

# --- 4. SETUP GRAFICO ---
fig = plt.figure(facecolor='black', figsize=(18, 10))
mng = plt.get_current_fig_manager()
try: mng.window.state('zoomed') 
except: pass

fig.suptitle("THE INFORMATION LATTICE: RIEMANN R-FUNCTION PROBE", color='#FF00FF', fontsize=26, fontweight='bold', y=0.96)
ax_lattice = fig.add_axes([0.50, 0.12, 0.46, 0.75], facecolor='black')
ax_lattice.set_axis_off()

def wrap_52(label, value):
    return f"{label}:\n{textwrap.fill(str(value), width=52)}\n\n"

info_str = "MONITORING SYSTEM PROBE\n" + "-"*48 + "\n\n"
info_str += wrap_52("N EVEN", N)
info_str += wrap_52("p1 (INTO LATTICE)", p1)
info_str += wrap_52("p2", p2)

# Sezione Distanza e Orizzonte
info_str += f"DISTANCE (p2 - p1): {distanza_primi}\n"
if fuori_range:
    info_str += "!! NOTE: p2 BEYOND THE VISIBLE HORIZON !!\n\n"
else:
    info_str += "STATUS: COMPLETE PAIR IN THE SECTOR\n\n"

info_str += "RIEMANN R-FUNCTION ANALYSIS:\n"
info_str += f"Expected primes (R): {stima_riemann:.2f}\n"
info_str += f"Real primes:      {len(green_indices)}\n"
info_str += f"Deviation:       {deviazione:+.4f}%\n\n"
info_str += "LEGEND: RED(Comp) GREEN(Primes) MAGENTA(Couple)\n" + "-"*48

txt_box = fig.text(0.04, 0.5, info_str, color='white', fontsize=8.2, family='monospace', va='center', ha='left',
                   bbox=dict(facecolor='#0a0a0a', edgecolor='#FF00FF', lw=2, pad=15))

x_coords, y_coords = [i % cols for i in range(n_total)], [rows - 1 - (i // cols) for i in range(n_total)]
scatter = ax_lattice.scatter(x_coords, y_coords, s=11, color='#111111', edgecolors='none')

# --- 5. CONTROLLI ---
ax_button = fig.add_axes([0.04, 0.07, 0.08, 0.04])
button = Button(ax_button, 'PAUSE', color='#151515', hovercolor='#333333')
button.label.set_color('white')

anim_running = True
def toggle_pause(event):
    global anim_running
    if anim_running: ani.event_source.stop(); button.label.set_text('PLAY')
    else: ani.event_source.start(); button.label.set_text('PAUSE')
    anim_running = not anim_running
button.on_clicked(toggle_pause)

def update(frame):
    current_colors = np.full((n_total, 3), 0.08)
    progress = frame * 750
    idx_r = [idx for idx in red_indices if idx < progress]
    current_colors[idx_r] = [0.8, 0.0, 0.0]
    if progress > n_total:
        prog_v = progress - n_total
        idx_v = [idx for idx in green_indices if idx < prog_v]
        current_colors[red_indices] = [0.8, 0.0, 0.0]
        current_colors[idx_v] = [0.0, 1.0, 0.0]
        if goldbach_indices:
            flicker = [1.0, 0.0, 1.0] if frame % 2 == 0 else [0.4, 0.0, 0.8]
            for g_idx in goldbach_indices:
                if g_idx < prog_v: current_colors[g_idx] = flicker
    scatter.set_facecolors(current_colors)
    return scatter,

ani = animation.FuncAnimation(fig, update, frames=(n_total*2)//750 + 60, interval=25, blit=True)
plt.show()

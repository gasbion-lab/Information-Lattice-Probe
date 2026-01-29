import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button
import numpy as np
import random
import textwrap
# Developed by Gasbion-lab | Part of the Information Lattice Field Theory (ILFT)
# --- 1. COMPUTATIONAL ENGINE (Miller-Rabin Primality Test) ---
def is_prime(n, k=10):
    
    """Rigorous primality test for high-magnitude integers."""
    if n <= 1: return False
    if n <= 3: return True
    if n % 2 == 0: return False
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

# --- 2. DATA ACQUISITION & GOLDBACH SYMMETRY SEARCH ---
print("-" * 50)
print("GASBION-LAB: GOLDBACH REFLEXIVE PROBE")
N_input = input("Enter a large EVEN integer to test Goldbach Symmetry: ")
try:
    N = eval(N_input)
except:
    N = 2**100 # Default fallback
if N % 2 != 0: N += 1

print(f"Searching for reflexive prime pairs (p1 + p2 = N)...")
found = False
d = 1 if (N//2) % 2 == 0 else 0
while not found:
    p1, p2 = (N // 2) - d, (N // 2) + d
    if is_prime(p1) and is_prime(p2): found = True
    else: d += 2

# Distance between the two primes
prime_distance = p2 - p1
out_of_range = prime_distance > 10000

# Centering the lattice around p1 for visual focus
y_start = ((p1 - 1) // 2) - 50

# --- 3. SECTOR ANALYSIS ---
rows, cols = 100, 100
n_total = rows * cols
red_indices, green_indices, goldbach_indices = [], [], []

for i in range(n_total):
    val = 2 * (y_start + i) + 1
    if val == p1 or val == p2: goldbach_indices.append(i)
    elif is_prime(val): green_indices.append(i)
    else: red_indices.append(i)

# --- 4. GRAPHICAL SETUP ---
fig = plt.figure(facecolor='black', figsize=(18, 10))
mng = plt.get_current_fig_manager()
try: mng.window.state('zoomed') 
except: pass

fig.suptitle("GOLDBACH CONJECTURE EXPLORER", color='#FF00FF', fontsize=28, fontweight='bold', y=0.95)
ax_lattice = fig.add_axes([0.50, 0.12, 0.46, 0.75], facecolor='black')
ax_lattice.set_axis_off()

def format_long_text(label, value, width=42):
    wrapped = textwrap.fill(str(value), width=width)
    return f"{label}:\n{wrapped}\n\n"

# Scientific Log Sidebar
info_str = "GOLDBACH SYMMETRY DEMONSTRATOR\n" + "-"*50 + "\n\n"
info_str += format_long_text("TARGET EVEN N", N)
info_str += format_long_text("SINGULARITY p1 (LATTICE FOCUS)", p1)
info_str += format_long_text("SINGULARITY p2", p2)

# Range Warning logic
info_str += f"STRUCTURAL DISTANCE (p2 - p1):\n{prime_distance}\n"
if out_of_range:
    info_str += "!! p2 BEYOND VISUAL HORIZON !!\n\n"
else:
    info_str += "REFLEXIVE PAIR WITHIN LATTICE RANGE\n\n"

info_str += "VISUAL LEGEND:\nRED: Composite Numbers\nGREEN: Prime Singularities\nMAGENTA: SYMMETRIC PAIR (FLICKER)\n" + "-"*40

txt_box = fig.text(0.04, 0.5, info_str, color='white', fontsize=9, 
                   family='monospace', va='center', ha='left',
                   wrap=True, linespacing=1.3,
                   bbox=dict(facecolor='#0a0a0a', edgecolor='#FF00FF', lw=2, pad=20))

x_coords = [i % cols for i in range(n_total)]
y_coords = [rows - 1 - (i // cols) for i in range(n_total)]
scatter = ax_lattice.scatter(x_coords, y_coords, s=11, color='#111111', edgecolors='none')

# --- 5. INTERACTIVE CONTROLS ---
anim_running = True
def toggle_pause(event):
    global anim_running
    anim_running = not anim_running
    if anim_running: ani.event_source.start()
    else: ani.event_source.stop()

ax_button = fig.add_axes([0.04, 0.07, 0.08, 0.04])
button = Button(ax_button, 'PAUSE', color='#151515', hovercolor='#333333')
button.label.set_color('white')
button.on_clicked(toggle_pause)

# --- 6. ANIMATION ENGINE ---
def update(frame):
    current_colors = np.full((n_total, 3), 0.08)
    progress = frame * 600
    
    # Phase 1: Composite background
    idx_r = [idx for idx in red_indices if idx < progress]
    current_colors[idx_r] = [0.8, 0.0, 0.0]
    
    # Phase 2: Prime singularities and Flicker effect
    if progress > n_total:
        prog_v = progress - n_total
        idx_v = [idx for idx in green_indices if idx < prog_v]
        current_colors[red_indices] = [0.8, 0.0, 0.0]
        current_colors[idx_v] = [0.0, 1.0, 0.0]
        
        if goldbach_indices:
            flicker_color = [1.0, 0.0, 1.0] if frame % 2 == 0 else [0.6, 0.0, 1.0]
            for g_idx in goldbach_indices:
                if g_idx < prog_v:
                    current_colors[g_idx] = flicker_color

    scatter.set_facecolors(current_colors)
    return scatter,

ani = animation.FuncAnimation(fig, update, frames=(n_total*2)//600 + 50, interval=30, blit=True)
plt.show()

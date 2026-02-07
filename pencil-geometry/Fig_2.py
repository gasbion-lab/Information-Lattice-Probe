import numpy as np
import matplotlib.pyplot as plt

def generate_lattice(limit):
    lattice = np.zeros(limit + 1, dtype=int)
    for k in range(3, int(2 * limit**0.5) + 3, 2):
        for x in range(1, limit):
            y = k * x + (k - 1) // 2
            if y <= limit:
                lattice[y] = 1
            else:
                break
    return lattice

# Configurazione parametri
LIMIT = 2000
lattice = generate_lattice(LIMIT)
positions = np.arange(LIMIT + 1)

# Uso di constrained_layout per gestire automaticamente gli spazi
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 16), constrained_layout=True)

# --- 1. DETERMINISTIC INFORMATION LATTICE ---
vis_limit = 80
colors = ['#1f77b4' if val == 0 else '#d62728' for val in lattice[:vis_limit]]
ax1.vlines(positions[:vis_limit], 0, lattice[:vis_limit], colors='gray', alpha=0.2)
ax1.scatter(positions[:vis_limit], lattice[:vis_limit], c=colors, s=50, zorder=3)
ax1.set_title("1. DETERMINISTIC INFORMATION LATTICE\n(Blue: Prime Gaps | Red: Composite Signals)", fontsize=15, pad=20)
ax1.set_ylim(-0.3, 1.3)
ax1.set_yticks([0, 1])
ax1.set_yticklabels(['GAP (Prime)', 'SIGNAL (Comp.)'], fontsize=11)
ax1.set_xlabel("Lattice Position (y)", labelpad=10)

# --- 2. GOLDBACH COUPLING CAPACITY ---
evens, couplings = [], []
for n_even in range(10, LIMIT, 2):
    count = 0
    y_target = (n_even // 2) - 1 
    for i in range(1, (y_target // 2) + 1):
        if lattice[i] == 0 and lattice[y_target - i] == 0:
            count += 1
    evens.append(n_even)
    couplings.append(count)

ax2.scatter(evens, couplings, s=4, color='navy', alpha=0.5, label="Prime Pairs")
# Soglia evidenziata meglio
ax2.axhline(y=min(couplings[30:]), color='red', linestyle='--', linewidth=2.5, label="Empirical Lower Bound")
ax2.set_title("2. GOLDBACH COUPLING CAPACITY\n(Lattice Sums: p1 + p2 = 2n)", fontsize=15, pad=20)
ax2.set_xlabel("Even Number (2n)", labelpad=10)
ax2.set_ylabel("Pair Counts", labelpad=10)
ax2.legend(loc="upper left", frameon=True, shadow=True)

# --- 3. TWIN PRIME STABILITY RATIO ---
indices, ratios = [], []
tp_count, p_count = 0, 0
for i in range(1, LIMIT):
    if lattice[i] == 0:
        p_count += 1
        if lattice[i-1] == 0: tp_count += 1
    if i % 50 == 0 and p_count > 2:
        indices.append(i)
        ratios.append(tp_count / (p_count / np.log(i+1)))

ax3.plot(indices, ratios, color='forestgreen', linewidth=2.5, label="Measured Stability")
ax3.axhline(y=1.0, color='black', linestyle='-', linewidth=1.5)
# Zona di stabilità più visibile
ax3.fill_between(indices, 0.8, 1.2, color='yellow', alpha=0.3, label="Ideal Stability Zone")
ax3.set_title("3. TWIN PRIME STABILITY RATIO\n(Persistence of Adjacent Lattice Gaps)", fontsize=15, pad=20)
ax3.set_xlabel("Lattice Range (n)", labelpad=10)
ax3.set_ylabel("Stability Index", labelpad=10)
ax3.set_ylim(0, 2.2)
ax3.legend(loc="upper right", frameon=True, shadow=True)

plt.show()

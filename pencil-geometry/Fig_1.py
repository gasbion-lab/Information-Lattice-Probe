import numpy as np
import matplotlib.pyplot as plt

def visualizza_geometria_reticolo(limit_y, max_k):
    plt.figure(figsize=(12, 8))
    
    # 1. Lattice plane setup
    y_coords = np.arange(1, limit_y + 1)
    lattice = np.zeros(limit_y + 1)

    # 2. Drawing composite trajectories (Information Waves)
    # Each k is a "signal generator"
    colors = plt.cm.viridis(np.linspace(0, 1, max_k))
    
    for k_idx, k in enumerate(range(3, max_k + 1, 2)):
        y_points = []
        x_points = []
        for x in range(1, limit_y):
            y = k * x + (k - 1) // 2
            if y <= limit_y:
                y_points.append(y)
                x_points.append(k)
                lattice[y] = 1
            else:
                break
        
        # Connect multiples of the same k
        plt.plot(y_points, x_points, 'o-', color=colors[k_idx], alpha=0.4, 
                 linewidth=1, markersize=4, label=f'k={k}' if k < 15 else "")

    # 3. Highlight Primes (Information Gaps/Singularities)
    primes_y = [y for y in range(1, limit_y + 1) if lattice[y] == 0]
    plt.vlines(primes_y, 0, max_k, colors='red', linestyles='dotted', 
                alpha=0.5, label='Primes (Singularities)')

    # 4. Formatting and Global Laws
    plt.title("Lattice Information Geometry: Composite Waves vs. Prime Gaps", fontsize=14)
    plt.xlabel("Lattice Position $y$ (Odd Integers)", fontsize=12)
    plt.ylabel("Generator $k$ (Wave Frequency)", fontsize=12)
    
    # Updated annotations with academic terminology
    plt.text(limit_y*0.02, max_k*0.9, "Riemann Spectral Law: Distribution of spectral gaps", 
             bbox=dict(facecolor='white', alpha=0.7))
    plt.text(limit_y*0.45, max_k*0.05, "Twin Prime Law: Persistence of adjacent singularities", 
             bbox=dict(facecolor='white', alpha=0.7))
    
    plt.grid(True, which='both', linestyle='--', alpha=0.2)
    plt.legend(loc='upper right', bbox_to_anchor=(1.15, 1))
    plt.tight_layout()
    
    return plt.gcf()

# Run for a clear view of the first 100 positions
fig = visualizza_geometria_reticolo(100, 30)
plt.show()

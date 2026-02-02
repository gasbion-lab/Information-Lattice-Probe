import matplotlib.pyplot as plt
import numpy as np

def generate_lattice_final_v2():
    limit_x = 12
    limit_y = 35 
    fig, ax = plt.subplots(figsize=(15, 10), facecolor='white')
    
    focus_x, focus_y = -0.5, -0.5
    
    # Primi 6 generatori (k = 3, 5, 7, 9, 11, 13)
    k_values = [3, 5, 7, 9, 11, 13]
    x_range = np.linspace(-1, limit_x, 300)
    
    all_composites_y = set()
    
    # Disegno del fascio e intersezioni esatte
    for k in k_values:
        y_line = k * x_range + (k - 1) / 2
        ax.plot(x_range, y_line, alpha=0.4, linewidth=1.5, zorder=1)
        
        for x in range(1, limit_x + 1):
            y = k * x + (k - 1) // 2
            if y <= limit_y:
                all_composites_y.add(y)
                ax.scatter(x, y, color='red', s=50, edgecolors='darkred', zorder=4)

    # Lacune (Numeri Primi)
    lattice_y = np.arange(1, limit_y + 1)
    primes_y = [p for p in lattice_y if p not in all_composites_y]
    
    for p in primes_y:
        ax.scatter(0, p, color='lime', s=120, edgecolors='black', zorder=5)

    # Riferimenti strutturali
    ax.axvline(x=0.5, color='blue', linestyle='--', linewidth=2)
    ax.scatter(focus_x, focus_y, color='black', s=250, zorder=10)

    # --- UNIFICAZIONE BOX DESTRA (Legenda + Formule) ---
    # Posizionata leggermente più in alto (va=bottom con y=2 o 3)
    info_text = (
        r"$\mathbf{Mathematical\ Framework}$" + "\n\n" +
        r"$\mathbf{Generator\ Function:}$" + "\n" +
        r"$y = kx + \frac{k-1}{2}$" + "\n\n" +
        r"$\mathbf{Integer\ Mapping:}$" + "\n" +
        r"$n = 2y + 1$" + "\n\n" +
        r"$\mathbf{Legend:}$" + "\n" +
        r"$\bullet$ Red nodes: Composites" + "\n" +
        r"$\bullet$ Green nodes: Prime Singularities" + "\n" +
        r"$\bullet$ Black Focus: $F(-1/2, -1/2)$" + "\n" +
        r"$\bullet$ Blue line: Riemann Axis (0.5)"
    )
    
    ax.text(limit_x - 0.2, 3, info_text, fontsize=11, color='black',
            bbox=dict(facecolor='#fdfdfd', alpha=0.95, edgecolor='navy', boxstyle='round,pad=1'),
            ha='right', va='bottom', zorder=10)

    # Titoli e Assi
    ax.set_title("DETERMINISTIC LATTICE: PENCIL FOCUS AND PRIME EMERGENCE", fontsize=16, fontweight='bold')
    ax.set_xlabel("x (Multiplier Index)", fontsize=12)
    ax.set_ylabel("y (Lattice Positions)", fontsize=12)
    
    # Griglia sui valori interi
    ax.set_xticks(np.arange(-1, limit_x + 1, 1))
    ax.set_yticks(np.arange(-1, limit_y + 1, 1))
    ax.grid(True, linestyle=':', alpha=0.4)
    
    ax.set_xlim(-1, limit_x)
    ax.set_ylim(-1, limit_y)

    plt.show()

generate_lattice_final_v2()

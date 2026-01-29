import matplotlib.pyplot as plt
import numpy as np
import random
import textwrap
import time

def is_prime_miller_rabin(n, k=25):
    `# Developed by Gasbion-lab | Part of the Information Lattice Field Theory (ILFT)`
    """Miller-Rabin Primality Test: Computational Engine."""
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

def format_long_number(n, width=30):
    """Wraps long integers for clear display within the information box."""
    return "\n".join(textwrap.wrap(str(n), width))

def plot_geometric_detection(y_input, y_found, offset, k_max=1000):
    """Visualizes the local lattice structure around the identified singularity."""
    y_min, y_max = y_found - offset, y_found + offset
    distance = y_found - y_input
    p1_full = 2 * y_found + 1
    p2_full = 2 * y_found + 3
    
    # Box width configuration
    chars = 42 

    fig, ax = plt.subplots(figsize=(18, 10))
    # Adjust margins for the side info-box and title
    plt.subplots_adjust(left=0.35, right=0.95, top=0.90, bottom=0.1)
    
    # Calculate Lattice points (background distribution)
    punti_x, punti_k = [], []
    for k in range(3, k_max + 1, 2):
        x_start = (y_min - (k - 1) // 2 + k - 1) // k
        curr_y = k * max(1, x_start) + (k - 1) // 2
        while curr_y <= y_max:
            if curr_y >= y_min:
                punti_x.append(curr_y - y_found)
                punti_k.append(k)
            curr_y += k

    # Render the Manifold structure
    ax.scatter(punti_x, punti_k, c=punti_k, cmap='viridis', alpha=0.4, s=15, edgecolors='none', zorder=2)
    
    # Red indicators for the identified Prime Singularity (Twin Pair)
    ax.scatter([0, 1], [0, 0], color='red', s=150, zorder=5, label="Singularity Detected")
    ax.axvline(x=0, color='red', ls=':', alpha=0.2, lw=1)
    ax.axvline(x=1, color='red', ls=':', alpha=0.2, lw=1)

    # Scientific Log Box Construction
    info_box = (
        f"GEOMETRIC DETECTION LOG\n"
        f"{'='*chars}\n\n"
        f"INPUT Y (ORIGIN):\n{format_long_number(y_input, chars)}\n\n"
        f"DETECTED SINGULARITY Y:\n{format_long_number(y_found, chars)}\n\n"
        f"STRUCTURAL DISTANCE:\n+{distance}\n\n"
        f"PRIME p1 (2y+1):\n{format_long_number(p1_full, chars)}\n\n"
        f"PRIME p2 (2y+3):\n{format_long_number(p2_full, chars)}\n\n"
        f"{'='*chars}\n"
        f"ENGINE: Miller-Rabin | k-max={k_max}"
    )
    
    # Sidebar positioning
    fig.text(0.02, 0.5, info_box, fontsize=9, family='monospace',
             va='center', ha='left', linespacing=1.6,
             bbox=dict(facecolor='#ffffff', alpha=1, edgecolor='#cc0000', boxstyle='round,pad=1'))

    ax.set_title("LOCAL LATTICE STRUCTURE: SINGULARITY ANALYSIS", fontsize=16, weight='bold')
    ax.set_xlim(-offset, offset)
    ax.set_xlabel(f"LATTICE COORDINATE (OFFSET FROM INPUT):\n+{distance}\n\n")
    ax.set_ylabel("Generator (k)")
    ax.grid(True, alpha=0.05)
    
    plt.show()

def main():
    try:
        # User input for the starting coordinate y
        valore = input("GASBION PROBE > Enter starting y coordinate (e.g., 10**16): ").strip().replace("^", "**")
        y_start = int(eval(valore))
        radius = 50 
        
        print(f"\nRadar Active... Scanning for singularities after y = {y_start}")
        y_check = y_start
        while True:
            # Checking for Twin Prime Singularity (2y+1, 2y+3)
            if is_prime_miller_rabin(2 * y_check + 1) and is_prime_miller_rabin(2 * y_check + 3):
                print(f"✅ Singularity detected at y = {y_check}")
                plot_geometric_detection(y_start, y_check, radius)
                break
            
            y_check += 1
            if (y_check - y_start) % 100000 == 0:
                print(f"Processed {y_check - y_start} indices...", end='\r')
                
    except KeyboardInterrupt:
        print("\nScan aborted by user.")
    except Exception as e:
        print(f"\nInput Error: {e}")

if __name__ == "__main__":
    while True:
        main()
        cont = input("Run another scan? (y/n): ").lower()
        if cont != 'y':
            break

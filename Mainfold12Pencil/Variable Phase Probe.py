import math
import random
import time
# Developed by Gasbion-lab | Part of the Information Lattice Field Theory (ILFT)
def miller_rabin(n, k=50): # Maximum precision for laboratory-grade testing
    if n <= 1: return False
    if n <= 3: return True
    if n % 2 == 0 or n % 3 == 0 or n % 5 == 0: return False
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

def drilling_resonance_350():
    # --- CONFIGURATION WITH USER INPUT ---
    print("\n--- DRILLING PARAMETERS CONFIGURATION ---")
    try:
        EXP = int(input("Enter Exponent (e.g., 500 for 10^500): "))
        TARGET_PHASE = float(input("Enter TARGET PHASE (e.g., 0.985): "))
        TOLERANCE = float(input("Enter TOLERANCE (e.g., 0.050): "))
        SCAN_RANGE = int(input("Enter STEP SCAN RANGE (e.g., 2000000): "))
    except ValueError:
        print("Error: Please enter valid numerical values.")
        return
    
    print("\n" + "█"*60)
    print(f"    --- COHERENT DRILLING: RESONANCE {TARGET_PHASE} ---")
    print(f"    --- ANALYSIS OVER {SCAN_RANGE} STEPS AT 10^{EXP} ---")
    print("█"*60)
    
    n_base = 10**EXP
    # Initializing from residue 11 mod 180
    p_start = n_base + (11 - (n_base % 180)) % 180
    
    # 1. Phase Selection Stage (Instantaneous)
    print(f"\n[1/2] Selecting targets within phase...")
    targets = []
    for i in range(SCAN_RANGE):
        # Calculating phase for each step using the Arcsine-Sine mapping
        phase = math.asin(math.sin(i / 100 + EXP))
        if abs(phase - TARGET_PHASE) < TOLERANCE:
            targets.append((i, phase))
    
    num_targets = len(targets)
    if num_targets == 0:
        print("No resonance points found with this tolerance. Try increasing it.")
        return

    print(f"Found {num_targets} resonance points out of {SCAN_RANGE} steps.")
    print(f"Computational Optimization: {((1 - num_targets/SCAN_RANGE)*100):.2f}%")
    
    # 2. Hunting Stage (Selective Miller-Rabin)
    print(f"\n[2/2] Commencing drilling of selected resonance points...\n")
    start_time = time.perf_counter()
    found_count = 0

    try:
        for idx, (step, effective_phase) in enumerate(targets):
            p = p_start + (step * 180)
            
            # Testing binary 11
            if miller_rabin(p):
                # If a prime is found, verify the constellation structure
                res = [True, miller_rabin(p+2), miller_rabin(p+6), miller_rabin(p+8)]
                hits = sum(res)
                
                if hits >= 2:
                    found_count += 1
                    # Labeling based on the number of primes in the cluster
                    constellation_type = "!!! QUADRUPLET !!!" if hits == 4 else ("TRIPLET" if hits == 3 else "TWIN")
                    print(f"\n[RESONANCE HIT] {constellation_type}")
                    print(f"STEP: {step} | PHASE: {effective_phase:+.5f}")
                    print(f"P-VALUE: {p}")
                    print("-" * 40)
            
            if (idx + 1) % 500 == 0:
                elapsed = time.perf_counter() - start_time
                print(f"Analyzed: {idx+1}/{num_targets} | Time: {elapsed:.1f}s | Found: {found_count}")

    except KeyboardInterrupt:
        print("\nDrilling process interrupted by user.")

    print(f"\nMission Complete. Resonance points analyzed: {num_targets}")
    print(f"Special targets intercepted on frequency {TARGET_PHASE}: {found_count}")

if __name__ == "__main__":
    drilling_resonance_350()

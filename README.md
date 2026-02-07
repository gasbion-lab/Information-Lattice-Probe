# Information Lattice Field Theory (ILFT) & Pencil Projections

[![10.5281](https://zenodo.org)](https://doi.org)](https://doi.org/10.5281/zenodo.18448347)

**Author:** Silvio Gabbianelli (gasbion-lab)


**Field:** Computational Number Theory, Information Physics, Projective Geometry



---



## 🔬 Project Overview

This repository hosts the **Information Lattice Probe**, a computational engine designed for the algorithmic implementation and formal documentation of the **Information Lattice Field Theory (ILFT)**. 



The project provides a deterministic geometric framework to analyze prime singularities, offering new insights into the Riemann Hypothesis, the Twin Prime Conjecture, and Goldbach’s Conjecture. Through the mapping function $\phi(n) = \frac{n-1}{2}$ and the **Pencil Projection** methodology, prime distribution is analyzed as a result of structural rigidity within a discrete informational manifold (Modulo-12).



---



## 🛠 Interactive Exploration Tools



The repository includes a suite of Python tools designed to visualize the geometric properties of the Information Lattice:



* **Lattice Explorer**: A wide-sector probe to visualize prime distribution (S-Points) vs. composite projections (P-Projections) across extreme numerical ranges.

* **Goldbach Reflexive Probe**: Demonstrates the reflexive symmetry of even targets $N$, identifying the $p_1, p_2$ pair as mirrored singularities within the M12 manifold.

* **Twin Singularity Radar**: A local-scale analyzer focused on the structural distance between primes, ideal for studying Twin Prime persistence and lattice rigidity.



### Quick Start
```bash
To run the probes, ensure you have `numpy` and `matplotlib` installed:

```

python probes/GoldbachSymmetry.py



## 📚 Scientific Publications

If you use this research or code, please cite the following works:



1. **The Unified Field of Singularities: Geometric Formalization via Pencil Projections** *Theorems 3.2 (Twin Primes) and 3.3 (Goldbach Reflexive Sum).* [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18399848.svg)](https://doi.org/10.5281/zenodo.18399848)



2. **Computational Analysis of a Mapping $\phi(n)$ for Prime Singularity Detection** *Foundational theory of the Information Lattice.* [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18378546.svg)](https://doi.org/10.5281/zenodo.18378546)



---



## 🛠 Software Modules

### 📐 Pencil Projection Analysis
The following visualization demonstrates the core mathematical engine of the ILFT. It maps the composite lines (Pencils) converging at the focal point $F(-0.5, -0.5)$ and the emergence of prime singularities along the informational corridors.

* **Source Code:** [`PencilProjectionPlotter.py`](./pencil-geometry/PencilProjectionPlotter.py)
* **Mathematical Basis:** $y = kx + \frac{k-1}{2}$

![`PencilProjectionPlotter.png`](./pencil-geometry/PencilProjectionPlotter.png)
*Figure 1: Structural map of the Information Lattice showing composite intersections and prime emergence.*

### 1. Lattice Core (The Original Probe)

The fundamental engine for mapping odd integers into the information lattice and detecting singularities.



### 2. Pencil Geometry (Advanced Piecewise Analysis)

Questa sezione contiene gli script Python sviluppati per validare e visualizzare la teoria della **Pencil Geometry** applicata al Manifold $\mathcal{M}_{12}$.

### 📊 Descrizione degli Script

#### 1. `Fig_1.py` - Lattice Information Geometry
Questo script genera la visualizzazione delle frequenze dei generatori $k$ all'interno del reticolo.
* **Analisi Spettrale**: Mostra come le "onde" dei composti (da $k=3$ a $k=13$) saturano il lattice $y$.
* **Singolarità**: Evidenzia i "gap" (spazi vuoti) che corrispondono matematicamente ai numeri primi, confermando la distribuzione spettrale delle lacune di Riemann.
* **Twin Prime Law**: Visualizza la persistenza delle singolarità adiacenti, fornendo una prova geometrica della stabilità dei primi gemelli.

#### 2. `Fig_2.py` - Deterministic Information Lattice
Uno strumento di analisi multi-pannello che elabora i dati estratti dal manifold su larga scala.
* **Signal vs Gap**: Mappa la distinzione binaria tra segnali deterministici (composti) e gap informativi (primi).
* **Goldbach Coupling**: Calcola e visualizza la capacità di accoppiamento del lattice, mostrando come ogni numero pari sia il risultato di una somma di posizioni "gap" nel manifold.
* **Twin Prime Stability**: Monitora l'indice di stabilità del rapporto tra primi gemelli e range del lattice, dimostrando la natura non casuale della loro distribuzione.

---

Located in `/pencil-geometry`, this module implements **piecewise linear trajectories (spezzate)** to visualize topological corridors and reflexive symmetries.



#### **Gasbion System: Focal Analysis Log Output**

```

ENGINE: MILLER-RABIN | FOCUS F(-0.5, -0.5)

GEN: y = kx + (k-1)/2 | PENCIL PROJECTION

......................................................

RIEMANN DENSITY R(x) (Sector): 264.71

ACTUAL SINGULARITIES FOUND: 243

STRUCTURAL DEVIATION: -8.2031%

......................................................

GOLDBACH TARGET N: 1298074214633706907132624082305024

p1 (SING.): 649037107316853453566312041147283

p2 (SING.): 649037107316853453566312041157741

......................................................

LINES: M12 Piecewise | RED: Pencil | MAGENTA: Goldbach

......................................................

......................................................

```

![Pencil Projection Analysis](pencil-geometry/gasbionRadar.png)







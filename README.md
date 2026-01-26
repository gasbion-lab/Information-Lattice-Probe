# Information-Lattice-Probe
Official implementation of the Information Lattice Field Theory (ILFT) for deterministic prime density analysis. Includes the Gasbion-Riemann Probe.
# Information Lattice Field Theory (ILFT) - Official Probe

This repository contains the computational framework and verification tools for the **Information Lattice Field Theory**, as presented in the paper: 
**"Computational Analysis of a Mapping ϕ(n) for Prime Singularity Detection"**.

## 📄 Research Paper
The full theory, including the formal proofs of the mapping $\phi(n) = (n-1)/2$ and the structural analysis of Goldbach and Riemann symmetries, is published and archived on Zenodo:

**DOI:** [10.5281/zenodo.18378546](https://doi.org/10.5281/zenodo.18378546)

## 🚀 The Gasbion-Riemann Probe
The core of this repository is the `Probe.py` script, a high-performance verification tool designed to:
* Map odd integers into the discrete information lattice $\mathcal{L}$.
* Identify prime singularities through the exclusion of composite generating functions.
* Verify prime density alignment with the Gram series at extreme depths ($10^{50}$ and beyond).

## 🛠 Installation & Usage
```bash
git clone [https://github.com/gasbion-lab/Information-Lattice-Probe.git](https://github.com/gasbion-lab/Information-Lattice-Probe.git)
cd Information-Lattice-Probe
python Probe.py

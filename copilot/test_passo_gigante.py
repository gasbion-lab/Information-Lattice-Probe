import math
import time

N = 208701896930419739418841
p_reale = 377131511947
q_reale = 553392889003

# Dati calcolati
m0 = math.isqrt(N) + 1
m_soluzione = (p_reale + q_reale) // 2

print("\n" + "="*75)
print("   TEST PASSO GIGANTE: 18 MILIARDI")
print("="*75)
print(f"• Semiprimo N              : {N}")
print(f"• m0 (√N)                  : {m0}")
print(f"• m_soluzione (vera)       : {m_soluzione}")
print(f"• Distanza dalla soluzione : {m_soluzione - m0}")
print("-----------------------------------------------------------------------\n")

def calcola_resto(m, N):
    """Calcola il resto: quanto siamo lontani da un quadrato perfetto"""
    d2 = (m * m) - N
    if d2 < 0:
        return float('inf')
    d = math.isqrt(d2)
    return d2 - (d * d)

# Passo gigante
PASSO_GIGANTE = 18_000_000_000

print(f"Passo gigante: {PASSO_GIGANTE:,}\n")
print(f"Avanzando da m0 = {m0} con passo di {PASSO_GIGANTE}:\n")

m = m0
for i in range(20):
    resto = calcola_resto(m, N)
    distanza_soluzione = abs(m - m_soluzione)
    
    print(f"[PASSO #{i}] m = {m:>20} | resto = {resto:>15} | distanza soluzione = {distanza_soluzione:>12}")
    
    # Cerca la soluzione esatta
    d2 = (m * m) - N
    if d2 >= 0:
        d = math.isqrt(d2)
        if d * d == d2:
            print(f"\n💥 SOLUZIONE TROVATA!")
            print(f"   m = {m}")
            print(f"   Passi totali: {i}")
            break
    
    m += PASSO_GIGANTE

print("\n" + "="*75)
print("ANALISI:")
print("="*75)
print(f"\nSe il resto 'torna indietro' (diminuisce) dopo il primo passo,")
print(f"significa che abbiamo superato la soluzione e possiamo usare")
print(f"una fisarmonica per trovarla!")

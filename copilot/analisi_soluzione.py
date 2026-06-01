import math

# Dati noti
N = 208701896930419739418841
p_reale = 377131511947
q_reale = 553392889003

# La formula di Fermat: m = (p + q) / 2
m_soluzione = (p_reale + q_reale) // 2
m0 = math.isqrt(N) + 1

print("="*75)
print("   ANALISI DELLA SOLUZIONE FERMAT")
print("="*75)
print(f"• N = {N}")
print(f"• p = {p_reale}")
print(f"• q = {q_reale}")
print(f"\n• m0 (√N) = {m0}")
print(f"• m_soluzione = (p+q)/2 = {m_soluzione}")
print(f"• Distanza: m - m0 = {m_soluzione - m0}")
print(f"\n• d = (q-p)/2 = {(q_reale - p_reale) // 2}")

# Verifica che è davvero la soluzione
d = m_soluzione - p_reale
print(f"\n• Verifica:")
print(f"  p = m - d = {m_soluzione} - {d} = {m_soluzione - d}")
print(f"  q = m + d = {m_soluzione} + {d} = {m_soluzione + d}")
print(f"  p × q = {(m_soluzione - d) * (m_soluzione + d)}")
print(f"  Corretto? {(m_soluzione - d) * (m_soluzione + d) == N}")

# Il punto di minimo trovato
m_minimo = 456839027973
print(f"\n• Punto di minimo trovato: {m_minimo}")
print(f"• Differenza dalla soluzione: {abs(m_soluzione - m_minimo)}")
print(f"• La soluzione è a {abs(m_soluzione - m_minimo)} passi dal minimo!")

import numpy as np
import matplotlib.pyplot as plt

def I(p, eps):
    # Añadimos un valor minúsculo para evitar log2(0)
    p = np.clip(p, 1e-10, 1-1e-10)
    eps = np.clip(eps, 1e-10, 1-1e-10)
    
    term1 = -(p + (1 - p) * eps) * np.log2(p + (1 - p) * eps)
    term2 = -((1 - p) * (1 - eps)) * np.log2((1 - p) * (1 - eps))
    term3 = (1 - p) * eps * np.log2(eps) + (1 - p) * (1 - eps) * np.log2(1 - eps)
    return term1 + term2 + term3

# 1. Usamos linspace para tener exactamente 200 puntos
eps_val = np.linspace(0.0025, 0.5, 200)
p_val = np.linspace(0, 1, 200)

# 2. Creamos una malla (mesh) para poder graficar en 3D o calor
# Esto es más eficiente que una lista de tuplas para graficar
P, EPS = np.meshgrid(p_val, eps_val)
Z = I(P, EPS)

# 3. Graficamos
plt.figure(figsize=(10, 7))
cp = plt.contourf(P, EPS, Z, levels=50, cmap='viridis')
# 2. CAPA DE RESALTADO ROJA SEMITRANSPARENTE
#levels=[0.5, Z.max() + 0.01] -> Define la zona desde 0.5 hasta el final.
#colors=[(1, 0, 0, 0.3)] -> R, G, B, Alpha. (Rojo con 30% de opacidad)
plt.contourf(P, EPS, Z, levels=[0.5, Z.max() + 0.01], colors=[(1, 0, 0, 0.3)])

# Opcional: Añadir también el borde blanco de la Opción 1 para más claridad
plt.contour(P, EPS, Z, levels=[0.5], colors='white', linewidths=2)

plt.colorbar(cp, label='I(p, eps)')
plt.title('Mapa de calor de I(p, eps)')
plt.xlabel('p')
plt.ylabel('epsilon')
plt.show()
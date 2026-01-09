import numpy as np
import matplotlib.pyplot as plt

def binary_entropy(p):
    p = np.clip(p, 1e-10, 1 - 1e-10)
    return -p * np.log2(p) - (1 - p) * np.log2(1 - p)

def mutual_information(e0, e1, p):
    """Calcula I(X,Y) donats els errors i la probabilitat de l'entrada p=P(X=0)."""
    # Probabilitat de rebre un zero a la sortida P(Y=0)
    py0 = p * (1 - e0) + (1 - p) * e1
    
    hy = binary_entropy(py0)
    hy_x = p * binary_entropy(e0) + (1 - p) * binary_entropy(e1)
    
    return hy - hy_x

# Configuració de la simulació
epsilon_vals = np.linspace(0, 0.99, 200)
E0, E1 = np.meshgrid(epsilon_vals, epsilon_vals)

# Valors de p a comparar (Probabilitat de transmetre un '0')
p_fonts = [0.1, 0.3, 0.5, 0.8]

fig, axes = plt.subplots(1, 4, figsize=(20, 5))
fig.suptitle('Regió on I(X,Y) > 0.5 per a diferents fonts (p)', fontsize=16)

for i, p in enumerate(p_fonts):
    # Calculem la Informació Mútua per a cada combinació d'errors amb aquesta p
    I = mutual_information(E0, E1, p)
    
    # Dibuixem la regió
    axes[i].contourf(E0, E1, I, levels=[0.5, 1.0], colors=['#ffcccb'], alpha=0.5)
    line = axes[i].contour(E0, E1, I, levels=[0.5], colors=['red'])
    
    axes[i].set_title(f'Font amb p(X=0) = {p}')
    axes[i].set_xlabel('Error $\epsilon_0$')
    if i == 0: axes[i].set_ylabel('Error $\epsilon_1$')
    axes[i].grid(True, alpha=0.3)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
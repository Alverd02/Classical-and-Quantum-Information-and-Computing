import numpy as np
import matplotlib.pyplot as plt

# Entropia binària
def H_b(q):
    q = np.clip(q, 1e-12, 1 - 1e-12)  # evitar log(0)
    return -q * np.log2(q) - (1 - q) * np.log2(1 - q)

# Informació mútua BSC
def mutual_information(p0, p):
    py0 = p0 * (1 - p) + (1 - p0) * p
    return H_b(py0) - H_b(p)

# Rang de valors
p0_vals = np.linspace(0, 1, 200)
p_vals = np.linspace(0, 0.5, 200)  # canal simètric

P0, P = np.meshgrid(p0_vals, p_vals)
I_vals = mutual_information(P0, P)

# ---- Gràfic 3D ----
fig = plt.figure(figsize=(14,6))

ax1 = fig.add_subplot(121, projection='3d')
ax1.plot_surface(P0, P, I_vals, cmap='viridis')
ax1.set_xlabel('$p_0$ (entrada 0)')
ax1.set_ylabel('$p$ (soroll)')
ax1.set_zlabel('$I(X;Y)$')
ax1.set_title('Informació mútua (superfície 3D)')

# ---- Gràfic 2D ----
ax2 = fig.add_subplot(122)
p_fixed_values = [0.0, 0.05, 0.1, 0.2, 0.3, 0.4]  # valors de soroll
for p in p_fixed_values:
    I_curve = mutual_information(p0_vals, p)
    ax2.plot(p0_vals, I_curve, label=f"$p$ = {p}")

ax2.set_xlabel('$p_0$ (entrada 0)')
ax2.set_ylabel('$I(X;Y)$ [bits]')
ax2.set_title('Seccions per valors fixos de $p$')
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.show()

import numpy as np
import matplotlib.pyplot as plt

def I(p, eps_0,eps_1):
    # Añadimos un valor minúsculo para evitar log2(0)
    p = np.clip(p, 1e-10, 1-1e-10)
    eps_0 = np.clip(eps_0, 1e-10, 1-1e-10)
    eps_1 = np.clip(eps_1, 1e-10, 1-1e-10)

    term1 = -(p*(1-eps_0)+ (1 - p) * eps_1) * np.log2(p*(1-eps_0) + (1 - p) * eps_1)
    term2 = -(p*eps_0+(1 - p) * (1 - eps_1)) * np.log2(p*eps_0+(1 - p) * (1 - eps_1))
    term3 = (1 - p) * eps_1 * np.log2(eps_1) + (1 - p) * (1 - eps_1) * np.log2(1 - eps_1)
    term4 = -p*(1-eps_0) * np.log2(1-eps_0) + p*eps_0 * np.log2(eps_0)
    return term1 + term2 + term3 + term4
def derI(p,eps_0,eps_1):
    p = np.clip(p, 1e-10, 1-1e-10)
    eps_0 = np.clip(eps_0, 1e-10, 1-1e-10)
    eps_1 = np.clip(eps_1, 1e-10, 1-1e-10)

    term1=(1-eps_0-eps_1)*np.log2((p*eps_0+(1-p)*(1-eps_1))/(p*(1-eps_0)+(1-p)*eps_1))
    term2=(1-eps_0)*np.log2(1-eps_0)+eps_0*np.log2(eps_0)
    term3=-eps_1*np.log2(eps_1)-(1-eps_1)*np.log2(1-eps_1)
    return term1 + term2 + term3
# 1. Usamos linspace para tener exactamente 200 puntos
eps_val = np.linspace(0.0025, 0.5, 200)


# 2. Creamos una malla (mesh) para poder graficar en 3D o calor
# Esto es más eficiente que una lista de tuplas para graficar
eps0, eps1 = np.meshgrid(eps_val, eps_val)
def bis(a,b,derI,eps_0,eps_1):
    epsilon = b-a
    while epsilon>0.02:
        c = (a+b)/2
        epsilon = b-a
        if derI(c,eps_0,eps_1)*derI(a,eps_0,eps_1) < 0:
            b=c
        if derI(c,eps_0,eps_1)*derI(b,eps_0,eps_1)<0:
            a=c
        if derI(c,eps_0,eps_1)==0:
            break
    return c

roots = np.zeros_like(eps0)

for i in range(eps0.shape[0]):
    for j in range(eps0.shape[1]):
        roots[i, j] = bis(0.0, 1.0,derI,eps0[i, j],eps1[i, j])

C = I(roots, eps0, eps1)


cp = plt.contourf(eps0, eps1,C, levels=50, cmap='viridis')

#plt.contourf(eps0, eps1,C, levels=[0.5, C.max() + 0.01], colors=[(1, 0, 0, 0.3)])
plt.contour(eps0, eps1,C, levels=[0.5], colors='white', linewidths=2)

plt.colorbar(cp, label='C')
plt.xlabel("eps_0")
plt.ylabel("eps_1")
plt.title("C")
plt.show()
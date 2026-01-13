import numpy as np
import matplotlib.pyplot as plt
import random
from matplotlib.patches import Rectangle
from matplotlib.widgets import TextBox, Button

def normalizar_estado(estado):
    """Normalitza l'estat quàntic"""
    norma = np.sqrt(np.sum(np.abs(estado)**2))
    return estado / norma

def probabilidad_medida(estado, base):
    """Calcula la probabilitat de cada resultat de mesura en una base donada"""
    if base == 'z':
        # Mesura en base z: |0⟩ i |1⟩
        p0 = np.abs(estado[0])**2 + np.abs(estado[1])**2
        p1 = np.abs(estado[2])**2 + np.abs(estado[3])**2
        return p0, p1
    else:
        # Mesura en base rotada (angle alpha)
        alpha = base
        # Probabilitat de +1 en el segon qubit
        p_plus = (np.abs(estado[0]*np.cos(alpha/2) + estado[1]*np.sin(alpha/2))**2 +
                 np.abs(estado[2]*np.cos(alpha/2) + estado[3]*np.sin(alpha/2))**2)
        # Probabilitat de -1 en el segon qubit
        p_minus = (np.abs(estado[0]*np.sin(alpha/2) - estado[1]*np.cos(alpha/2))**2 +
                  np.abs(estado[2]*np.sin(alpha/2) - estado[3]*np.cos(alpha/2))**2)
        return p_plus, p_minus

def simular_medida_quantica(estado, alpha, n_simulaciones):
    """Simula n mesures quàntiques de l'estat"""
    estado = normalizar_estado(estado)
    resultados = {'++': 0, '+-': 0, '-+': 0, '--': 0}
    valores_A = []
    valores_B = []

    for _ in range(n_simulaciones):
        # Mesura primer qubit en base z
        p0, p1 = probabilidad_medida(estado, 'z')
        rand1 = random.random()
        if rand1 < p0:
            resultado_A = 1
            # Col·lapse estat: només components [0],[1]
            norm = np.sqrt(np.abs(estado[0])**2 + np.abs(estado[1])**2)
            estado_colapsat = np.array([estado[0], estado[1], 0, 0]) / norm if norm != 0 else np.array([0,0,0,0])
        else:
            resultado_A = -1
            norm = np.sqrt(np.abs(estado[2])**2 + np.abs(estado[3])**2)
            estado_colapsat = np.array([0, 0, estado[2], estado[3]]) / norm if norm != 0 else np.array([0,0,0,0])

        # Mesura segon qubit en base alpha
        p_plus, p_minus = probabilidad_medida(estado_colapsat, alpha)
        rand2 = random.random()
        if rand2 < p_plus:
            resultado_B = 1
        else:
            resultado_B = -1

        # Registrem els resultats
        if resultado_A == 1 and resultado_B == 1:
            resultados['++'] += 1
        elif resultado_A == 1 and resultado_B == -1:
            resultados['+-'] += 1
        elif resultado_A == -1 and resultado_B == 1:
            resultados['-+'] += 1
        else:
            resultados['--'] += 1

        valores_A.append(resultado_A)
        valores_B.append(resultado_B)

    # Calculem valors promig
    A_avg = np.mean(valores_A)
    B_avg = np.mean(valores_B)
    sum_avg = np.mean([a + b for a, b in zip(valores_A, valores_B)])
    prod_avg = np.mean([a * b for a, b in zip(valores_A, valores_B)])

    # Calculem percentatges
    total = n_simulaciones
    percentatges = {
        '%++': resultados['++'] / total * 100,
        '%+-': resultados['+-'] / total * 100,
        '%-+': resultados['-+'] / total * 100,
        '%--': resultados['--'] / total * 100
    }

    return resultados, percentatges, A_avg, B_avg, sum_avg, prod_avg

def calcular_probabilidades_teoricas(estado, alpha):
    """Calcula les probabilitats teòriques"""
    estado = normalizar_estado(estado)
    p_plus_plus = np.abs(estado[0]*np.cos(alpha/2) + estado[1]*np.sin(alpha/2))**2
    p_plus_minus = np.abs(estado[0]*np.sin(alpha/2) - estado[1]*np.cos(alpha/2))**2
    p_minus_plus = np.abs(estado[2]*np.cos(alpha/2) + estado[3]*np.sin(alpha/2))**2
    p_minus_minus = np.abs(estado[2]*np.sin(alpha/2) - estado[3]*np.cos(alpha/2))**2
    return [p_plus_plus, p_plus_minus, p_minus_plus, p_minus_minus]

def calcular_valors_esperats_teorics(estado, alpha):
    """Calcula els valors esperats teòrics"""
    estado = normalizar_estado(estado)
    E_prod = (np.abs(estado[0]*np.cos(alpha/2) + estado[1]*np.sin(alpha/2))**2 +
              np.abs(estado[2]*np.sin(alpha/2) - estado[3]*np.cos(alpha/2))**2 -
              np.abs(estado[0]*np.sin(alpha/2) - estado[1]*np.cos(alpha/2))**2 -
              np.abs(estado[2]*np.cos(alpha/2) + estado[3]*np.sin(alpha/2))**2)
    E_A = (np.abs(estado[0])**2 + np.abs(estado[1])**2 -
           np.abs(estado[2])**2 - np.abs(estado[3])**2)
    E_B = (np.abs(estado[0]*np.cos(alpha/2) + estado[1]*np.sin(alpha/2))**2 +
           np.abs(estado[2]*np.cos(alpha/2) + estado[3]*np.sin(alpha/2))**2 -
           np.abs(estado[0]*np.sin(alpha/2) - estado[1]*np.cos(alpha/2))**2 -
           np.abs(estado[2]*np.sin(alpha/2) - estado[3]*np.cos(alpha/2))**2)
    return E_A, E_B, E_prod

def visualizar_experimento(alpha, resultados, percentatges, A_avg, B_avg, sum_avg, prod_avg, 
                          probs_teoricas, estado, n_simulaciones):
    """Visualitza l'experiment i els resultats"""
    fig = plt.figure(figsize=(16, 10))

    # Diagrama detectors SG
    ax1 = fig.add_subplot(2, 2, 1)
    ax1.set_xlim(-2, 6)
    ax1.set_ylim(-2, 2)
    ax1.set_aspect('equal')
    ax1.axis('off')
    ax1.set_title('Configuració experimental', fontsize=14, fontweight='bold')
    ax1.add_patch(Rectangle((0, -0.5), 1, 1, fill=True, color='lightblue'))
    ax1.text(0.5, -1.2, 'SG-z', ha='center', va='center', fontsize=12)
    ax1.arrow(1.5, 0, 0.5, 0, head_width=0.2, head_length=0.1, fc='k', ec='k')
    ax1.add_patch(Rectangle((3, -0.5), 1, 1, fill=True, color='lightgreen'))
    ax1.text(3.5, -1.2, f'SG-α (α={np.degrees(alpha):.1f}°)', ha='center', va='center', fontsize=12)
    ax1.plot([3, 4], [0, 0], 'k-', lw=2)
    ax1.arrow(4.5, 0, 0.5*np.cos(alpha), 0.5*np.sin(alpha), head_width=0.2, head_length=0.1, fc='k', ec='k')
    ax1.text(0.5, 1.2, f'+1: {resultados["++"]+resultados["+-"]} | -1: {resultados["-+"]+resultados["--"]}', 
             ha='center', va='center', fontsize=11, bbox=dict(facecolor='lightblue', alpha=0.7))
    ax1.text(3.5, 1.2, f'+1: {resultados["++"]+resultados["-+"]} | -1: {resultados["+-"]+resultados["--"]}', 
             ha='center', va='center', fontsize=11, bbox=dict(facecolor='lightgreen', alpha=0.7))

    # Histograma de resultats combinats
    ax2 = fig.add_subplot(2, 2, 2)
    combinaciones = ['++', '+-', '-+', '--']
    counts = [resultados['++'], resultados['+-'], resultados['-+'], resultados['--']]
    teoricos = [p * n_simulaciones for p in probs_teoricas]
    x = np.arange(len(combinaciones))
    width = 0.35
    ax2.bar(x - width/2, counts, width, label='Observat', color='skyblue')
    ax2.bar(x + width/2, teoricos, width, label='Teòric', color='orange', alpha=0.7)
    ax2.set_xlabel('Resultats')
    ax2.set_ylabel('Comptatge')
    ax2.set_title('Resultats combinats dels detectors')
    ax2.set_xticks(x)
    ax2.set_xticklabels(combinaciones)
    ax2.legend()
    for i, v in enumerate(counts):
        ax2.text(i - width/2, v + 0.01, f'{counts[i]/n_simulaciones*100:.1f}%', ha='center', va='bottom')
    for i, v in enumerate(teoricos):
        ax2.text(i + width/2, v + 0.01, f'{teoricos[i]/n_simulaciones*100:.1f}%', ha='center', va='bottom', color='orange')

    # Valors promig i CHSH
    ax3 = fig.add_subplot(2, 2, 3)
    ax3.axis('off')
    E_A_teoric, E_B_teoric, E_prod_teoric = calcular_valors_esperats_teorics(estado, alpha)
    texto = f"""
    ESTAT NORMALITZAT:
    [{estado[0]:.3f}, {estado[1]:.3f}, {estado[2]:.3f}, {estado[3]:.3f}]
    
    RESULTATS OBSERVATS (n={n_simulaciones}):
    +1,+1: {resultados['++']} ({percentatges['%++']:.1f}%)
    +1,-1: {resultados['+-']} ({percentatges['%+-']:.1f}%)
    -1,+1: {resultados['-+']} ({percentatges['%-+']:.1f}%)
    -1,-1: {resultados['--']} ({percentatges['%--']:.1f}%)
    
    VALORS PROMIG OBSERVATS:
    SG-z: {A_avg:.3f} (esperat: {E_A_teoric:.3f})
    SG-α: {B_avg:.3f} (esperat: {E_B_teoric:.3f})
    Suma: {sum_avg:.3f} (esperat: {E_A_teoric + E_B_teoric:.3f})
    Producte: {prod_avg:.3f} (esperat: {E_prod_teoric:.3f})
    """
    ax3.text(0.1, 0.9, texto, ha='left', va='top', fontfamily='monospace', fontsize=10)

    # Verificació de la desigualtat CHSH
    ax4 = fig.add_subplot(2, 2, 4)
    ax4.axis('off')
    texto_chsh = f"""
    DESIGUALTAT CHSH:
    S = E(a,b) - E(a,b') + E(a',b) + E(a',b')
    
    Per a α=0, el valor del producte és: {prod_avg:.3f}
    
    Límit clàssic: |S| ≤ 2
    Límit quàntic: |S| ≤ 2√2 ≈ 2.828
    
    NOTA: Per veure la violació CHSH completa, caldria simular
    amb diferents angles (0°, 45°, 90°, 135°) i calcular S.
    """
    ax4.text(0.1, 0.7, texto_chsh, ha='left', va='top', fontfamily='monospace', fontsize=10)

    plt.tight_layout()
    plt.show()

# ...existing code...

def mostrar_resultats(estado, alpha, n_simulaciones):
    estado_normalizado = normalizar_estado(estado)
    resultados, percentatges, A_avg, B_avg, sum_avg, prod_avg = simular_medida_quantica(
        estado_normalizado, alpha, n_simulaciones)
    probs_teoricas = calcular_probabilidades_teoricas(estado_normalizado, alpha)
    visualizar_experimento(alpha, resultados, percentatges, A_avg, B_avg, sum_avg, prod_avg,
                           probs_teoricas, estado_normalizado, n_simulaciones)

def main():
    def executar(event):
        try:
            a = float(text_a_real.text) + 1j * float(text_a_imag.text)
            b = float(text_b_real.text) + 1j * float(text_b_imag.text)
            c = float(text_c_real.text) + 1j * float(text_c_imag.text)
            d = float(text_d_real.text) + 1j * float(text_d_imag.text)
            estado = np.array([a, b, c, d])
            alpha = np.radians(float(text_alpha.text))
            n_simulaciones = int(text_nsim.text)
            mostrar_resultats(estado, alpha, n_simulaciones)
        except Exception as e:
            print(f"Error: {e}")

    fig, ax = plt.subplots(figsize=(6, 6))
    plt.subplots_adjust(left=0.3, bottom=0.5)
    ax.axis('off')
    ax.set_title("Introdueix els paràmetres de la simulació", fontsize=14)

    axbox_a_real = plt.axes([0.05, 0.8, 0.15, 0.05])
    text_a_real = TextBox(axbox_a_real, 'a (real)', initial="1")
    axbox_a_imag = plt.axes([0.22, 0.8, 0.15, 0.05])
    text_a_imag = TextBox(axbox_a_imag, 'a (imag)', initial="0")

    axbox_b_real = plt.axes([0.05, 0.72, 0.15, 0.05])
    text_b_real = TextBox(axbox_b_real, 'b (real)', initial="0")
    axbox_b_imag = plt.axes([0.22, 0.72, 0.15, 0.05])
    text_b_imag = TextBox(axbox_b_imag, 'b (imag)', initial="0")

    axbox_c_real = plt.axes([0.05, 0.64, 0.15, 0.05])
    text_c_real = TextBox(axbox_c_real, 'c (real)', initial="0")
    axbox_c_imag = plt.axes([0.22, 0.64, 0.15, 0.05])
    text_c_imag = TextBox(axbox_c_imag, 'c (imag)', initial="0")

    axbox_d_real = plt.axes([0.05, 0.56, 0.15, 0.05])
    text_d_real = TextBox(axbox_d_real, 'd (real)', initial="0")
    axbox_d_imag = plt.axes([0.22, 0.56, 0.15, 0.05])
    text_d_imag = TextBox(axbox_d_imag, 'd (imag)', initial="0")

    axbox_alpha = plt.axes([0.05, 0.48, 0.32, 0.05])
    text_alpha = TextBox(axbox_alpha, 'α (graus)', initial="0")

    axbox_nsim = plt.axes([0.05, 0.40, 0.32, 0.05])
    text_nsim = TextBox(axbox_nsim, 'Simulacions', initial="1000")

    axbutton = plt.axes([0.15, 0.30, 0.15, 0.07])
    button = Button(axbutton, 'Simula')
    button.on_clicked(executar)

    plt.show()

if __name__ == "__main__":
    main()
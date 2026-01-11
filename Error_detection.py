import random

def simular_canal(epsilon, N=100000):

    errors_4bits = 0
    for _ in range(N):
        fallada = any(random.random() < epsilon for _ in range(4))
        if fallada:
            errors_4bits += 1
    
    perc_corruptes_4 = (errors_4bits / N) * 100

    fallades_5bits = 0
    detectats = 0
    for _ in range(N):

        n_errors = sum(1 for _ in range(5) if random.random() < epsilon)
        
        if n_errors > 0:
            fallades_5bits += 1
            if n_errors % 2 != 0:
                detectats += 1
                
    perc_corruptes_5 = (fallades_5bits / N) * 100
    perc_detectats_sobre_errors = (detectats / fallades_5bits) * 100

    return perc_corruptes_4, perc_detectats_sobre_errors

# Execució per epsilon = 0.1
e1 = 0.1
p4, p_det = simular_canal(e1)

print(f"Resultats per epsilon = {e1}:")
print(f"- Símbols corruptes (4 bits): {p4:.2f}% (Teòric: 34.39%)")
print(f"- Dels que fallen (5 bits), detectats: {p_det:.2f}% (Teòric: 82.09%)")

import random

def simular_shannon_asimmetric(epsilon_1, N=100000):
    alfabet = [
        (1/2, 0),    # x0: 0
        (1/4, 1),    # x1: 10
        (1/8, 2),    # x2: 110
        (1/16, 3),   # x3: 1110
        (1/32, 4),   # x4: 11110
        (1/64, 5),   # x5: 111110
        (1/128, 6),  # x6: 1111110
        (1/128, 7)   # x7: 1111111
    ]
    
    simbols_corruptes = 0
    
    for _ in range(N):
        r = random.random()
        acumulada = 0
        n_uns = 0
        
        for prob, uns in alfabet:
            acumulada += prob
            if r < acumulada:
                n_uns = uns
                break
        
        ha_fallat = False
        for _ in range(n_uns):
            if random.random() < epsilon_1:
                ha_fallat = True
                break
        
        if ha_fallat:
            simbols_corruptes += 1
            
    return (simbols_corruptes / N) * 100

# Execució
e1 = 0.1
percentatge = simular_shannon_asimmetric(e1)

print(f"Resultat Exercici 1 (Shannon) amb epsilon_1 = {e1} i epsilon_0 = 0:")
print(f"Símbols corruptes: {percentatge:.2f}%")
print(f"Teòric calculat abans: ~9.05%")

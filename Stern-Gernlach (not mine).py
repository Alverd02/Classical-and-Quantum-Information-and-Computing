import tkinter as tk
from tkinter import ttk
import numpy as np
import random

# --- Constants de la Interfície ---
BG_COLOR = "#f0f0f0"
CANVAS_WIDTH = 450
CANVAS_HEIGHT = 600
MAGNET_WIDTH = 100
MAGNET_HEIGHT = 200
MAGNET_GAP = 40
SCREEN_X = CANVAS_WIDTH - 50

class SternGerlachApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Simulador d'Experiment de Stern-Gerlach (Espí 1/2)")
        self.master.configure(bg=BG_COLOR)
        
        # --- Variables d'Estat ---
        self.c_up = 1.0 + 0.0j
        self.c_down = 0.0 + 0.0j
        self.prob_up = 1.0
        self.prob_down = 0.0

        # --- Interfície ---
        self.create_widgets()
        self.draw_apparatus()
        self.update_and_calculate()

    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.master, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # --- Canvas per a la visualització ---
        self.canvas = tk.Canvas(main_frame, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="white", highlightthickness=0)
        self.canvas.grid(row=0, column=0, rowspan=20, padx=(0, 20))

        # --- Panell de Control ---
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        ttk.Label(control_frame, text="Estat Inicial: |ψ⟩ = c_up|z,+⟩ + c_down|z,–⟩", font=("Helvetica", 12, "bold")).grid(row=0, column=0, columnspan=3, pady=(0, 10))

        # Entrades per c_up
        ttk.Label(control_frame, text="c_up:").grid(row=1, column=0, sticky=tk.W)
        self.c_up_real_var = tk.StringVar(value="1.0")
        self.c_up_imag_var = tk.StringVar(value="0.0")
        ttk.Entry(control_frame, textvariable=self.c_up_real_var, width=8).grid(row=1, column=1)
        ttk.Label(control_frame, text="+ i *").grid(row=1, column=2)
        ttk.Entry(control_frame, textvariable=self.c_up_imag_var, width=8).grid(row=1, column=3)

        # Entrades per c_down
        ttk.Label(control_frame, text="c_down:").grid(row=2, column=0, sticky=tk.W)
        self.c_down_real_var = tk.StringVar(value="0.0")
        self.c_down_imag_var = tk.StringVar(value="0.0")
        ttk.Entry(control_frame, textvariable=self.c_down_real_var, width=8).grid(row=2, column=1)
        ttk.Label(control_frame, text="+ i *").grid(row=2, column=2)
        ttk.Entry(control_frame, textvariable=self.c_down_imag_var, width=8).grid(row=2, column=3)
        
        # Botó d'actualització
        ttk.Button(control_frame, text="Actualitzar i Calcular", command=self.update_and_calculate).grid(row=3, column=0, columnspan=4, pady=10)

        # Separador
        ttk.Separator(control_frame, orient='horizontal').grid(row=4, column=0, columnspan=4, sticky='ew', pady=10)

        # Resultats teòrics
        ttk.Label(control_frame, text="Resultats Teòrics", font=("Helvetica", 12, "bold")).grid(row=5, column=0, columnspan=4)
        
        self.prob_up_label = ttk.Label(control_frame, text="P(z,+) = 1.0")
        self.prob_up_label.grid(row=6, column=0, columnspan=4, sticky=tk.W)
        
        self.prob_down_label = ttk.Label(control_frame, text="P(z,–) = 0.0")
        self.prob_down_label.grid(row=7, column=0, columnspan=4, sticky=tk.W)

        self.exp_val_label = ttk.Label(control_frame, text="⟨σ_z⟩ = 1.0")
        self.exp_val_label.grid(row=8, column=0, columnspan=4, sticky=tk.W, pady=(10,0))
        
        self.std_dev_label = ttk.Label(control_frame, text="Δσ_z = 0.0")
        self.std_dev_label.grid(row=9, column=0, columnspan=4, sticky=tk.W)

        # Separador
        ttk.Separator(control_frame, orient='horizontal').grid(row=10, column=0, columnspan=4, sticky='ew', pady=10)
        
        # Panell de simulació
        ttk.Label(control_frame, text="Simulació", font=("Helvetica", 12, "bold")).grid(row=11, column=0, columnspan=4)
        ttk.Label(control_frame, text="Nº de simulacions (n):").grid(row=12, column=0, columnspan=2, sticky=tk.W)
        self.n_sim_var = tk.StringVar(value="1000")
        ttk.Entry(control_frame, textvariable=self.n_sim_var, width=10).grid(row=12, column=2, columnspan=2, sticky=tk.W)
        
        ttk.Button(control_frame, text="Executar Simulació", command=self.run_simulation).grid(row=13, column=0, columnspan=4, pady=10)

        self.sim_mean_label = ttk.Label(control_frame, text="Mitjana (sim) = N/A")
        self.sim_mean_label.grid(row=14, column=0, columnspan=4, sticky=tk.W)
        
        self.sim_std_label = ttk.Label(control_frame, text="Desviació (sim) = N/A")
        self.sim_std_label.grid(row=15, column=0, columnspan=4, sticky=tk.W)
        
        self.sim_counts_label = ttk.Label(control_frame, text="Comptes: ↑=N/A, ↓=N/A")
        self.sim_counts_label.grid(row=16, column=0, columnspan=4, sticky=tk.W, pady=(5,0))


    def draw_apparatus(self):
        # Eix z
        self.canvas.create_line(20, CANVAS_HEIGHT/2, 20, 50, arrow=tk.LAST)
        self.canvas.create_text(20, 40, text="z", font=("Helvetica", 12))
        
        # Iman Superior (Pol Nord)
        x0, y0 = 50, CANVAS_HEIGHT/2 - MAGNET_GAP/2 - MAGNET_HEIGHT
        x1, y1 = x0 + MAGNET_WIDTH, y0 + MAGNET_HEIGHT
        self.canvas.create_polygon(x0, y0, x1, y0, x1, y1, x0-20, y1, fill="red", outline="black")
        self.canvas.create_text(x0 + MAGNET_WIDTH/2, y0 + MAGNET_HEIGHT/2, text="N", font=("Helvetica", 20, "bold"), fill="white")

        # Iman Inferior (Pol Sud)
        x0, y0 = 50, CANVAS_HEIGHT/2 + MAGNET_GAP/2
        x1, y1 = x0 + MAGNET_WIDTH, y0 + MAGNET_HEIGHT
        self.canvas.create_polygon(x0-20, y0, x1, y0, x1, y1, x0, y1, fill="blue", outline="black")
        self.canvas.create_text(x0 + MAGNET_WIDTH/2, y0 + MAGNET_HEIGHT/2, text="S", font=("Helvetica", 20, "bold"), fill="white")

        # Pantalla de detecció
        self.canvas.create_line(SCREEN_X, 50, SCREEN_X, CANVAS_HEIGHT - 50, width=3)
        self.canvas.create_text(SCREEN_X, 35, text="Pantalla", font=("Helvetica", 10))

    def update_and_calculate(self):
        try:
            c_up_r = float(self.c_up_real_var.get())
            c_up_i = float(self.c_up_imag_var.get())
            c_down_r = float(self.c_down_real_var.get())
            c_down_i = float(self.c_down_imag_var.get())
        except ValueError:
            # Si l'entrada no és un número, no fa res
            return

        c_up = c_up_r + 1j * c_up_i
        c_down = c_down_r + 1j * c_down_i
        
        # Normalització de l'estat
        norm = np.sqrt(np.abs(c_up)**2 + np.abs(c_down)**2)
        if norm == 0:
            return # Evita divisió per zero
        
        self.c_up = c_up / norm
        self.c_down = c_down / norm
        
        # Actualitzar entrades amb valors normalitzats
        self.c_up_real_var.set(f"{self.c_up.real:.4f}")
        self.c_up_imag_var.set(f"{self.c_up.imag:.4f}")
        self.c_down_real_var.set(f"{self.c_down.real:.4f}")
        self.c_down_imag_var.set(f"{self.c_down.imag:.4f}")

        # Càlcul de probabilitats
        self.prob_up = np.abs(self.c_up)**2
        self.prob_down = np.abs(self.c_down)**2

        # Actualitzar labels de probabilitat
        self.prob_up_label.config(text=f"P(z,+) = {self.prob_up:.4f}")
        self.prob_down_label.config(text=f"P(z,–) = {self.prob_down:.4f}")
        
        # Càlculs teòrics (prenent valors +/- 1 per a σ_z)
        # Valor esperat: ⟨σ_z⟩ = (+1)*P(up) + (-1)*P(down)
        exp_val = self.prob_up - self.prob_down
        self.exp_val_label.config(text=f"⟨σ_z⟩ = {exp_val:.4f}")

        # Variància: Var(σ_z) = ⟨σ_z²⟩ - ⟨σ_z⟩² = 1 - ⟨σ_z⟩²
        # ja que σ_z² és la identitat, i ⟨I⟩ = 1
        variance = 1 - exp_val**2
        std_dev = np.sqrt(variance)
        self.std_dev_label.config(text=f"Δσ_z = {std_dev:.4f}")

        self.draw_trajectories()
        
    def draw_trajectories(self):
        # Esborrar trajectòries anteriors
        self.canvas.delete("trajectory")
        
        start_x = 180
        start_y = CANVAS_HEIGHT / 2
        
        end_y_up = CANVAS_HEIGHT / 2 - 150
        end_y_down = CANVAS_HEIGHT / 2 + 150

        # Gruix de la línia proporcional a la probabilitat
        width_up = 1 + 8 * self.prob_up
        width_down = 1 + 8 * self.prob_down

        # Dibuixar trajectòria cap amunt
        self.canvas.create_line(start_x, start_y, SCREEN_X, end_y_up, 
                                width=width_up, fill="#ff6666", tags="trajectory")
        
        # Dibuixar trajectòria cap avall
        self.canvas.create_line(start_x, start_y, SCREEN_X, end_y_down, 
                                width=width_down, fill="#6666ff", tags="trajectory")

    def run_simulation(self):
        try:
            n_sims = int(self.n_sim_var.get())
            if n_sims <= 0: return
        except ValueError:
            return

        # Fem 'n' mesures. El resultat és +1 (up) o -1 (down).
        # np.random.choice és molt eficient per a això.
        outcomes = np.random.choice([1, -1], size=n_sims, p=[self.prob_up, self.prob_down])
        
        # Càlcul de les estadístiques de la simulació
        sim_mean = np.mean(outcomes)
        sim_std = np.std(outcomes)
        
        count_up = np.sum(outcomes == 1)
        count_down = n_sims - count_up
        
        # Actualitzar labels de la simulació
        self.sim_mean_label.config(text=f"Mitjana (sim) = {sim_mean:.4f}")
        self.sim_std_label.config(text=f"Desviació (sim) = {sim_std:.4f}")
        self.sim_counts_label.config(text=f"Comptes: ↑={count_up}, ↓={count_down}")


if __name__ == "__main__":
    root = tk.Tk()
    app = SternGerlachApp(root)
    root.mainloop()
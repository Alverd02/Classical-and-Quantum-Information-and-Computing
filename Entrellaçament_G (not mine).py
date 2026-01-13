import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class EntanglementVisualizer:
    def __init__(self, master):
        self.master = master
        self.master.title("Visualitzador d'Evolució d'Entrellaçament (H = C S1·S2)")
        self.master.geometry("1000x800")

        # --- Paràmetres de la física (simplifiquem C*hbar = 1) ---
        self.omega = 1.0
        self.t_max = 4 * np.pi
        self.time_points = np.linspace(0, self.t_max, 400)

        # --- Calculem l'evolució sencera ---
        self.c01 = np.cos(self.omega * self.time_points / 2)
        self.c10 = -1j * np.sin(self.omega * self.time_points / 2)
        self.prob01 = np.abs(self.c01)**2
        self.prob10 = np.abs(self.c10)**2
        self.concurrence = np.abs(np.sin(self.omega * self.time_points))

        # --- Configuració de la GUI ---
        main_frame = ttk.Frame(self.master)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- Creació de la figura i els subplots de Matplotlib ---
        self.fig = Figure(figsize=(10, 7), dpi=100)
        self.ax_probs = self.fig.add_subplot(3, 1, 1)
        self.ax_concurrence = self.fig.add_subplot(3, 1, 2)
        self.ax_state_bar = self.fig.add_subplot(3, 1, 3)
        self.fig.tight_layout(pad=3.0)

        self.canvas = FigureCanvasTkAgg(self.fig, master=main_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # --- Slider de temps ---
        self.time_slider = ttk.Scale(main_frame, from_=0, to=self.t_max, orient=tk.HORIZONTAL)
        self.time_slider.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        # --- Dibuix inicial I connexió del slider (ORDRE CORREGIT) ---
        # 1. Dibuixa els gràfics estàtics i crea els atributs .prob_line etc.
        self.setup_static_plots() 
        
        # 2. Ara que els atributs existeixen, connecta el command del slider
        self.time_slider.config(command=self.update_plots)
        
        # 3. Posa el valor inicial del slider i actualitza el gràfic manualment
        self.time_slider.set(0)
        self.update_plots(0)

    def setup_static_plots(self):
        # Gràfic de probabilitats
        self.ax_probs.plot(self.time_points, self.prob01, 'b-', label=r'$P(|\uparrow\downarrow\rangle) = |\cos(\omega t/2)|^2$')
        self.ax_probs.plot(self.time_points, self.prob10, 'r--', label=r'$P(|\downarrow\uparrow\rangle) = |\sin(\omega t/2)|^2$')
        self.ax_probs.set_title("Evolució de les Probabilitats dels Estats Base")
        self.ax_probs.set_ylabel("Probabilitat")
        self.ax_probs.set_ylim(-0.1, 1.1)
        self.ax_probs.legend()
        self.ax_probs.grid(True, linestyle=':')

        # Gràfic de concurrència
        self.ax_concurrence.plot(self.time_points, self.concurrence, 'g-', label=r'$\mathcal{C}(t) = |\sin(\omega t)|$')
        self.ax_concurrence.set_title("Evolució de l'Entrellaçament (Concurrència)")
        self.ax_concurrence.set_xlabel("Temps (t) en unitats de 1/ω")
        self.ax_concurrence.set_ylabel("Concurrència")
        self.ax_concurrence.set_ylim(-0.1, 1.1)
        self.ax_concurrence.legend()
        self.ax_concurrence.grid(True, linestyle=':')

        # Línies verticals per al cursor de temps
        self.prob_line = self.ax_probs.axvline(0, color='k', linestyle='--')
        self.concurrence_line = self.ax_concurrence.axvline(0, color='k', linestyle='--')

    def update_plots(self, time_val_str):
        time_val = float(time_val_str)
        
        # Actualitza les línies verticals
        self.prob_line.set_xdata([time_val, time_val])
        self.concurrence_line.set_xdata([time_val, time_val])
        
        # Troba l'índex de temps més proper
        idx = (np.abs(self.time_points - time_val)).argmin()
        
        # Valors actuals
        p01 = self.prob01[idx]
        p10 = self.prob10[idx]
        conc = self.concurrence[idx]

        # Actualitza el títol del gràfic de barres
        title = (f"Estat a t={time_val:.2f}:  "
                 f"P(|↑↓⟩)={p01:.2f}, P(|↓↑⟩)={p10:.2f}  |  "
                 f"Concurrència={conc:.2f}")

        # Actualitza el gràfic de barres
        self.ax_state_bar.clear()
        labels = [r'$|\uparrow\uparrow\rangle$', r'$|\uparrow\downarrow\rangle$', r'$|\downarrow\uparrow\rangle$', r'$|\downarrow\downarrow\rangle$']
        probs = [0, p01, p10, 0]
        self.ax_state_bar.bar(labels, probs, color=['gray', 'blue', 'red', 'gray'])
        self.ax_state_bar.set_title(title)
        self.ax_state_bar.set_ylabel("Probabilitat")
        self.ax_state_bar.set_ylim(0, 1.1)
        
        # Redibuixa el canvas
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = EntanglementVisualizer(root)
    root.mainloop()
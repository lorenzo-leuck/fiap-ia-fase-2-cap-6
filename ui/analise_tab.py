import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

import subalgoritmos.clima as clima
import subalgoritmos.analise as analise
from utils import CULTURAS

class AnaliseTab(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.configurar_aba()
    
    def configurar_aba(self):
        frame = ttk.LabelFrame(self, text="Análise de Impacto Climático")
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ttk.Label(frame, text="Selecione a cultura para análise:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        
        self.analise_cultura_var = tk.StringVar(value="0")
        cultura_frame = ttk.Frame(frame)
        cultura_frame.grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
        ttk.Radiobutton(cultura_frame, text="Soja", variable=self.analise_cultura_var, value="0").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(cultura_frame, text="Milho", variable=self.analise_cultura_var, value="1").pack(side=tk.LEFT, padx=5)
        
        ttk.Button(frame, text="Realizar Análise", command=self.realizar_analise_impacto).grid(row=1, column=0, columnspan=2, pady=15)
        
        ttk.Label(frame, text="Resultado da Análise:").grid(row=2, column=0, sticky=tk.NW, padx=10, pady=5)
        self.analise_text = scrolledtext.ScrolledText(frame, width=80, height=20, wrap=tk.WORD)
        self.analise_text.grid(row=3, column=0, columnspan=2, sticky=tk.EW, padx=10, pady=5)
        self.analise_text.config(state=tk.DISABLED)
    
    def realizar_analise_impacto(self):
        try:
            cultura_id = int(self.analise_cultura_var.get())
            cultura_nome = CULTURAS[cultura_id]
            
            dados = clima.obter_dados_climaticos(self.app.latitude, self.app.longitude)
            if not dados:
                messagebox.showerror("Erro", "Não foi possível obter dados climáticos para análise.")
                return
            
            resultado_analise = analise.analisar_cultura(dados, cultura_id)
            
            self.analise_text.config(state=tk.NORMAL)
            self.analise_text.delete(1.0, tk.END)
            self.analise_text.insert(tk.END, f"Análise para: {cultura_nome}\n\n")
            self.analise_text.insert(tk.END, resultado_analise)
            self.analise_text.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao realizar análise: {str(e)}")

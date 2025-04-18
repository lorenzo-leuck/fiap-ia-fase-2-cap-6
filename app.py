import tkinter as tk
from tkinter import ttk, messagebox

from ui.entrada_tab import EntradaTab
from ui.dados_tab import DadosTab
from ui.clima_tab import ClimaTab
from ui.analise_tab import AnaliseTab
from subalgoritmos.db import DatabaseManager

class FarmTechApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("FarmTech Solutions - Monitoramento Agrícola")
        self.geometry("1000x700")
        self.configure(bg="#f0f0f0")
        
        self.dados_salvos = []
        
        self.db_path = "farmtech_solutions.sqlite"
        self.db_manager = DatabaseManager(self.db_path)
        
        self.latitude = -30.0277
        self.longitude = -51.2287
        
        self.criar_interface()
        
        self.after(100, self.inicializar_interface)
    
    def carregar_dados(self):
        try:
            self.dados_salvos = self.db_manager.carregar_dados()
            self.tab_dados.atualizar_dados(self.dados_salvos)
            self.tab_clima.atualizar_lista_lotes(self.dados_salvos)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar dados: {str(e)}")
    
    def criar_interface(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.tab_entrada = EntradaTab(self.notebook, self)
        self.tab_dados = DadosTab(self.notebook, self)
        self.tab_clima = ClimaTab(self.notebook, self)
        self.tab_analise = AnaliseTab(self.notebook, self)
        
        self.notebook.add(self.tab_entrada, text="Entrada de Dados")
        self.notebook.add(self.tab_dados, text="Dados")
        self.notebook.add(self.tab_clima, text="Dados Climáticos")
        self.notebook.add(self.tab_analise, text="Análise de Impacto")
    
    def inicializar_interface(self):
        self.carregar_dados()
        self.tab_clima.buscar_dados_climaticos()

if __name__ == "__main__":
    print("Iniciando interface FarmTech Solutions - Rio Grande do Sul...")
    app = FarmTechApp()
    app.mainloop()

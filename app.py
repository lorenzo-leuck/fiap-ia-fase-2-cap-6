import tkinter as tk
from tkinter import ttk

from ui.entrada_tab import EntradaTab
from ui.dados_tab import DadosTab
from ui.clima_tab import ClimaTab
from ui.analise_tab import AnaliseTab
from subalgoritmos.db import DatabaseManager
import subalgoritmos.clima as clima

class FarmTechApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("FarmTech Solutions - Monitoramento Agrícola")
        self.geometry("1000x700")
        self.configure(bg="#f0f0f0")
        
        self.dados_salvos = []
        self.dados_clima = None
        self.dados_atuais_formatados = None
        self.dados_historicos_formatados = None
        
        self.db_path = "farmtech_solutions.sqlite"
        self.db_manager = DatabaseManager(self.db_path)
        
        self.latitude = -30.0277
        self.longitude = -51.2287
        
        self.carregar_todos_dados()
        
        self.criar_interface()
    
    def carregar_todos_dados(self):
        try:
            self.dados_salvos = self.db_manager.carregar_dados()
        except Exception as e:
            print(f"Erro ao carregar dados do banco: {str(e)}")
            self.dados_salvos = []
        
        try:
            self.dados_clima = clima.obter_dados_climaticos(self.latitude, self.longitude)
            if self.dados_clima:
                _, self.dados_atuais_formatados = clima.formatar_dados_atuais(self.dados_clima)
                _, self.dados_historicos_formatados = clima.formatar_dados_historicos(self.dados_clima)
        except Exception as e:
            print(f"Erro ao carregar dados climáticos: {str(e)}")
            self.dados_clima = None
    
    def criar_interface(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.tab_entrada = EntradaTab(self.notebook, self)
        self.tab_dados = DadosTab(self.notebook, self)
        self.tab_clima = ClimaTab(self.notebook, self)
        self.tab_analise = AnaliseTab(self.notebook, self)
        
        if self.dados_salvos:
            self.tab_dados.atualizar_dados(self.dados_salvos)
        
        if self.dados_clima:
            self.tab_clima.inicializar_com_dados(self.dados_clima, self.dados_atuais_formatados, self.dados_historicos_formatados)
        
        self.notebook.add(self.tab_entrada, text="Entrada de Dados")
        self.notebook.add(self.tab_dados, text="Lotes")
        self.notebook.add(self.tab_clima, text="Clima")
        self.notebook.add(self.tab_analise, text="Análise")

if __name__ == "__main__":
    print("Iniciando interface FarmTech Solutions - Rio Grande do Sul...")
    print("Carregando dados, por favor aguarde...")
    app = FarmTechApp()
    app.mainloop()

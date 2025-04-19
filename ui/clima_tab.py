import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

import subalgoritmos.clima as clima

class ClimaTab(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.db_manager = app.db_manager
        self.latitude = app.latitude
        self.longitude = app.longitude
        self.tab_clima = self
        self.configurar_aba_clima()
    
    def configurar_aba_clima(self):
        frame = ttk.LabelFrame(self.tab_clima, text="Dados Climáticos para Monitoramento de Soja")
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        atual_frame = ttk.LabelFrame(frame, text="Condições Climáticas Atuais")
        atual_frame.pack(fill="x", padx=10, pady=10)
        
        self.clima_atual_text = scrolledtext.ScrolledText(atual_frame, width=60, height=8, wrap=tk.WORD)
        self.clima_atual_text.pack(fill="both", expand=True, padx=10, pady=10)
        self.clima_atual_text.config(state=tk.DISABLED)
        
        dados_frame = ttk.LabelFrame(frame, text="Dados Climáticos")
        dados_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        switch_frame = ttk.Frame(dados_frame)
        switch_frame.pack(fill="x", padx=10, pady=5)
        
        self.modo_exibicao = tk.StringVar(value="historico")
        ttk.Radiobutton(switch_frame, text="Histórico (7 dias)", variable=self.modo_exibicao, 
                       value="historico", command=self.alternar_modo_exibicao).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(switch_frame, text="Previsão (7 dias)", variable=self.modo_exibicao, 
                       value="previsao", command=self.alternar_modo_exibicao).pack(side=tk.LEFT, padx=10)
        
        colunas = ("data", "temp_max", "temp_min", "precipitacao", "clima")
        self.tabela_clima = ttk.Treeview(dados_frame, columns=colunas, show="headings", height=10)
        
        self.tabela_clima.heading("data", text="Data")
        self.tabela_clima.heading("temp_max", text="Temp. Máx. (°C)")
        self.tabela_clima.heading("temp_min", text="Temp. Mín. (°C)")
        self.tabela_clima.heading("precipitacao", text="Precipitação (mm)")
        self.tabela_clima.heading("clima", text="Condição")
        
        self.tabela_clima.column("data", width=100)
        self.tabela_clima.column("temp_max", width=100)
        self.tabela_clima.column("temp_min", width=100)
        self.tabela_clima.column("precipitacao", width=100)
        self.tabela_clima.column("clima", width=200)
        
        scrollbar = ttk.Scrollbar(dados_frame, orient=tk.VERTICAL, command=self.tabela_clima.yview)
        self.tabela_clima.configure(yscroll=scrollbar.set)
        
        self.tabela_clima.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        
        ttk.Button(frame, text="Salvar Dados Climáticos no Banco", command=self.salvar_dados_climaticos).pack(pady=10)
    
    def buscar_dados_climaticos(self):
        try:
            self.dados_clima = clima.obter_dados_climaticos(self.latitude, self.longitude)
            if not self.dados_clima:
                messagebox.showerror("Erro", "Não foi possível obter dados climáticos.")
                return
            
            self.exibir_clima_atual(self.dados_clima)
            
            self.alternar_modo_exibicao()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar dados climáticos: {str(e)}")
    
    def alternar_modo_exibicao(self):
        try:
            if not hasattr(self, 'dados_clima') or not self.dados_clima:
                return
                
            for item in self.tabela_clima.get_children():
                self.tabela_clima.delete(item)
            
            modo = self.modo_exibicao.get()
            
            if modo == "historico":
                dados_tabela, self.dados_historicos_formatados = clima.formatar_dados_historicos(self.dados_clima)
                titulo = "Histórico Climático (7 dias)"
            else:
                dados_tabela = clima.formatar_dados_previsao(self.dados_clima)
                titulo = "Previsão Climática (7 dias)"
            
            for dado in dados_tabela:
                self.tabela_clima.insert("", "end", values=(
                    dado["data"],
                    dado["temp_max"],
                    dado["temp_min"],
                    dado["precipitacao"],
                    dado["clima"]
                ))
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao alternar modo de exibição: {str(e)}")
    
    def exibir_clima_atual(self, dados):
        try:
            texto, self.dados_atuais_formatados = clima.formatar_dados_atuais(dados)
            
            self.clima_atual_text.config(state=tk.NORMAL)
            self.clima_atual_text.delete(1.0, tk.END)
            self.clima_atual_text.insert(tk.END, texto)
            self.clima_atual_text.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exibir clima atual: {str(e)}")
    
    def exibir_historico_climatico(self, dados):
        try:
            for item in self.tabela_clima.get_children():
                self.tabela_clima.delete(item)
            
            dados_tabela, self.dados_historicos_formatados = clima.formatar_dados_historicos(dados)
            
            for dado in dados_tabela:
                self.tabela_clima.insert("", "end", values=(
                    dado["data"],
                    dado["temp_max"],
                    dado["temp_min"],
                    dado["precipitacao"],
                    dado["clima"]
                ))
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exibir histórico climático: {str(e)}")
    

    
    def salvar_dados_climaticos(self):
        try:
            if not hasattr(self, 'dados_atuais_formatados') or not hasattr(self, 'dados_historicos_formatados'):
                messagebox.showerror("Erro", "Nenhum dado climático disponível para salvar.")
                return
            
            mensagem = self.db_manager.salvar_dados_climaticos(
                self.dados_atuais_formatados,
                self.dados_historicos_formatados
            )
            
            messagebox.showinfo("Sucesso", mensagem)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar dados climáticos: {str(e)}")
    
    def inicializar_interface(self):
        self.after(500, self.buscar_dados_climaticos)
        
    def atualizar_lista_lotes(self, dados_salvos=None):
        pass
        
    def atualizar_lista_lotes_deletar(self, dados_salvos=None):
        pass
        
    def listar_dados(self):
        pass


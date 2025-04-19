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
        """Configura a aba de dados climáticos"""
        frame = ttk.LabelFrame(self.tab_clima, text="Dados Climáticos para Monitoramento de Soja")
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Frame para dados atuais
        atual_frame = ttk.LabelFrame(frame, text="Condições Climáticas Atuais")
        atual_frame.pack(fill="x", padx=10, pady=10)
        
        self.clima_atual_text = scrolledtext.ScrolledText(atual_frame, width=60, height=8, wrap=tk.WORD)
        self.clima_atual_text.pack(fill="both", expand=True, padx=10, pady=10)
        self.clima_atual_text.config(state=tk.DISABLED)
        
        # Frame para histórico
        historico_frame = ttk.LabelFrame(frame, text="Histórico Climático (14 dias)")
        historico_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Criar tabela para histórico climático
        colunas = ("data", "temp_max", "temp_min", "precipitacao", "clima")
        self.tabela_clima = ttk.Treeview(historico_frame, columns=colunas, show="headings", height=10)
        
        # Configurar cabeçalhos
        self.tabela_clima.heading("data", text="Data")
        self.tabela_clima.heading("temp_max", text="Temp. Máx. (°C)")
        self.tabela_clima.heading("temp_min", text="Temp. Mín. (°C)")
        self.tabela_clima.heading("precipitacao", text="Precipitação (mm)")
        self.tabela_clima.heading("clima", text="Condição")
        
        # Configurar larguras das colunas
        self.tabela_clima.column("data", width=100)
        self.tabela_clima.column("temp_max", width=100)
        self.tabela_clima.column("temp_min", width=100)
        self.tabela_clima.column("precipitacao", width=100)
        self.tabela_clima.column("clima", width=200)
        
        # Adicionar scrollbar
        scrollbar = ttk.Scrollbar(historico_frame, orient=tk.VERTICAL, command=self.tabela_clima.yview)
        self.tabela_clima.configure(yscroll=scrollbar.set)
        
        # Posicionar tabela e scrollbar
        self.tabela_clima.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        
        # Botão para salvar dados no banco
        ttk.Button(frame, text="Salvar Dados Climáticos no Banco", command=self.salvar_dados_climaticos).pack(pady=10)
    
    def buscar_dados_climaticos(self):
        """Busca dados climáticos da API e exibe na interface"""
        try:
            # Buscar dados da API usando o módulo clima com as coordenadas padrão
            dados = clima.obter_dados_climaticos(self.latitude, self.longitude)
            if not dados:
                messagebox.showerror("Erro", "Não foi possível obter dados climáticos.")
                return
            
            # Exibir dados atuais
            self.exibir_clima_atual(dados)
            
            # Exibir histórico
            self.exibir_historico_climatico(dados)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar dados climáticos: {str(e)}")
    
    def exibir_clima_atual(self, dados):
        """Exibe os dados climáticos atuais"""
        try:
            # Usar o módulo clima para formatar os dados
            texto, self.dados_atuais_formatados = clima.formatar_dados_atuais(dados)
            
            # Exibir no widget de texto
            self.clima_atual_text.config(state=tk.NORMAL)
            self.clima_atual_text.delete(1.0, tk.END)
            self.clima_atual_text.insert(tk.END, texto)
            self.clima_atual_text.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exibir clima atual: {str(e)}")
    
    def exibir_historico_climatico(self, dados):
        """Exibe o histórico climático na tabela"""
        try:
            # Limpar a tabela existente
            for item in self.tabela_clima.get_children():
                self.tabela_clima.delete(item)
            
            # Usar o módulo clima para formatar os dados
            dados_tabela, self.dados_historicos_formatados = clima.formatar_dados_historicos(dados)
            
            # Preencher a tabela
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
        """Salva os dados climáticos no banco de dados"""
        try:
            if not hasattr(self, 'dados_atuais_formatados') or not hasattr(self, 'dados_historicos_formatados'):
                messagebox.showerror("Erro", "Nenhum dado climático disponível para salvar.")
                return
            
            # Usar o módulo db para salvar os dados
            mensagem = self.db_manager.salvar_dados_climaticos(
                self.dados_atuais_formatados,
                self.dados_historicos_formatados
            )
            
            messagebox.showinfo("Sucesso", mensagem)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar dados climáticos: {str(e)}")
    
    # Método para inicializar a interface, chamado externamente se necessário
    def inicializar_interface(self):
        """Inicializa os componentes da interface após a criação"""
        # Buscar dados climáticos iniciais
        self.after(500, self.buscar_dados_climaticos)
        
    def atualizar_lista_lotes(self, dados_salvos=None):
        """Método vazio para compatibilidade com app.py"""
        # Este método existe apenas para evitar erros no app.py
        pass
        
    def atualizar_lista_lotes_deletar(self, dados_salvos=None):
        """Método vazio para compatibilidade com app.py"""
        # Este método existe apenas para evitar erros no app.py
        pass
        
    def listar_dados(self):
        """Método vazio para compatibilidade com app.py"""
        # Este método existe apenas para evitar erros no app.py
        pass


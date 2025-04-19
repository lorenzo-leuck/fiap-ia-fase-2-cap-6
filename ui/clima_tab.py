import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import datetime

import subalgoritmos.clima as clima

class ClimaTab(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.db_manager = app.db_manager
        self.latitude = app.latitude
        self.longitude = app.longitude
        self.tab_clima = self
        self.dados_clima = None
        self.dados_atuais_formatados = None
        self.dados_historicos_formatados = None
        self.configurar_aba_clima()
    
    def configurar_aba_clima(self):
        frame = ttk.LabelFrame(self.tab_clima, text="Dados Climáticos para Monitoramento")
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
            
    def inicializar_com_dados(self, dados_clima, dados_atuais_formatados, dados_historicos_formatados):
        self.dados_clima = dados_clima
        self.dados_atuais_formatados = dados_atuais_formatados
        self.dados_historicos_formatados = dados_historicos_formatados
        
        if self.dados_clima:
            # Exibir dados já carregados
            self.exibir_clima_atual_com_dados(self.dados_atuais_formatados)
            self.alternar_modo_exibicao()
    
    def exibir_clima_atual_com_dados(self, dados_atuais_formatados):
        try:
            self.dados_atuais_formatados = dados_atuais_formatados
            
            self.clima_atual_text.config(state=tk.NORMAL)
            self.clima_atual_text.delete(1.0, tk.END)
            
            # Criar texto para exibição
            data_hora = datetime.datetime.fromisoformat(dados_atuais_formatados["data"].replace('Z', '+00:00')).strftime("%d/%m/%Y %H:%M")
            
            texto = f"Data e hora: {data_hora}\n"
            texto += f"Condição: {dados_atuais_formatados['descricao_clima']}\n"
            texto += f"Temperatura: {dados_atuais_formatados['temperatura']}°C\n"
            texto += f"Umidade: {dados_atuais_formatados.get('umidade', 'N/A')}%\n"
            texto += f"Precipitação: {dados_atuais_formatados['precipitacao']} mm\n"
            texto += f"Velocidade do vento: {dados_atuais_formatados.get('velocidade_vento', 'N/A')} km/h\n"
            
            # Verificar se existem dados de lote cadastrados
            tem_dados_lote = bool(self.app.dados_salvos)
            
            if tem_dados_lote:
                # Se tem dados de lote, adicionar informações sobre o estado da plantação
                temp_atual = dados_atuais_formatados['temperatura']
                umidade_atual = dados_atuais_formatados.get('umidade', 50)  # Valor padrão se não existir
                
                self.clima_atual_text.insert(tk.END, texto)
                self.clima_atual_text.insert(tk.END, "\n\nEstado da plantação baseado nos sensores:\n")
                
                # Verificar temperatura
                if temp_atual > 30:
                    self.clima_atual_text.insert(tk.END, f"\n⚠️ Temperatura alta pode prejudicar o desenvolvimento.")
                elif temp_atual < 15:
                    self.clima_atual_text.insert(tk.END, f"\n⚠️ Temperatura baixa pode retardar o crescimento.")
                else:
                    self.clima_atual_text.insert(tk.END, f"\n✅ Temperatura adequada para o desenvolvimento.")
                
                # Verificar umidade
                if umidade_atual > 80:
                    self.clima_atual_text.insert(tk.END, f"\n⚠️ Umidade muito alta, risco de doenças fúngicas.")
                elif umidade_atual < 30:
                    self.clima_atual_text.insert(tk.END, f"\n⚠️ Umidade muito baixa, pode ser necessário irrigação.")
                else:
                    self.clima_atual_text.insert(tk.END, f"\n✅ Umidade adequada para o desenvolvimento.")
            else:
                # Se não tem dados de lote, mostrar apenas informações climáticas
                self.clima_atual_text.insert(tk.END, texto)
            
            self.clima_atual_text.config(state=tk.DISABLED)
            
        except Exception as e:
            print(f"Erro ao exibir clima atual com dados: {str(e)}")
    
    def buscar_dados_climaticos(self):
        try:
            self.dados_clima = clima.obter_dados_climaticos(self.latitude, self.longitude)
            if not self.dados_clima:
                return
            
            self.exibir_clima_atual(self.dados_clima)
            self.alternar_modo_exibicao()
            
        except Exception as e:
            print(f"Erro ao buscar dados climáticos: {str(e)}")
    
    def alternar_modo_exibicao(self):
        try:
            if not hasattr(self, 'dados_clima') or not self.dados_clima:
                return
                
            for item in self.tabela_clima.get_children():
                self.tabela_clima.delete(item)
            
            modo = self.modo_exibicao.get()
            
            if modo == "historico":
                dados_tabela, self.dados_historicos_formatados = clima.formatar_dados_historicos(self.dados_clima)
            else:
                dados_tabela = clima.formatar_dados_previsao(self.dados_clima)
            
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
            
            # Verificar se existem dados de lote cadastrados
            tem_dados_lote = bool(self.app.dados_salvos)
            
            if tem_dados_lote:
                # Se tem dados de lote, adicionar informações sobre o estado da plantação
                temp_atual = dados.get('current', {}).get('temperature_2m', 0)
                umidade_atual = dados.get('current', {}).get('relative_humidity_2m', 0)
                
                self.clima_atual_text.insert(tk.END, texto)
                self.clima_atual_text.insert(tk.END, "\n\nEstado da plantação baseado nos sensores:\n")
                
                # Verificar temperatura
                if temp_atual > 30:
                    self.clima_atual_text.insert(tk.END, f"\n⚠️ Temperatura alta pode prejudicar o desenvolvimento.")
                elif temp_atual < 15:
                    self.clima_atual_text.insert(tk.END, f"\n⚠️ Temperatura baixa pode retardar o crescimento.")
                else:
                    self.clima_atual_text.insert(tk.END, f"\n✅ Temperatura adequada para o desenvolvimento.")
                
                # Verificar umidade
                if umidade_atual > 80:
                    self.clima_atual_text.insert(tk.END, f"\n⚠️ Umidade muito alta, risco de doenças fúngicas.")
                elif umidade_atual < 30:
                    self.clima_atual_text.insert(tk.END, f"\n⚠️ Umidade muito baixa, pode ser necessário irrigação.")
                else:
                    self.clima_atual_text.insert(tk.END, f"\n✅ Umidade adequada para o desenvolvimento.")
            else:
                # Se não tem dados de lote, mostrar apenas informações climáticas
                self.clima_atual_text.insert(tk.END, texto)
            
            self.clima_atual_text.config(state=tk.DISABLED)
            
        except Exception as e:
            print(f"Erro ao exibir clima atual: {str(e)}")
    
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


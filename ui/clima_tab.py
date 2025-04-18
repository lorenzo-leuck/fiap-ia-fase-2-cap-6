import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

import subalgoritmos.clima as clima
from utils import CULTURAS, calcular_area, calcular_insumos

class ClimaTab(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.indice_selecionado = None
        self.dados_atuais_formatados = None
        self.configurar_aba()
    
    def configurar_aba(self):
        frame = ttk.LabelFrame(self, text="Dados Climáticos")
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ttk.Label(frame, text="Selecione o lote a ser atualizado:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        
        self.lotes_combobox = ttk.Combobox(frame, width=40, state="readonly")
        self.lotes_combobox.grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
        self.lotes_combobox.bind("<<ComboboxSelected>>", self.carregar_dados_lote)
        
        ttk.Button(frame, text="Atualizar Lista", command=self.atualizar_lista_lotes).grid(row=0, column=2, padx=5, pady=5)
        
        edicao_frame = ttk.LabelFrame(frame, text="Editar Informações")
        edicao_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky=tk.EW)
        
        ttk.Label(edicao_frame, text="Novo nome do lote (deixe em branco para manter o atual):").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        self.novo_nome_lote_entry = ttk.Entry(edicao_frame, width=40)
        self.novo_nome_lote_entry.grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
        
        ttk.Label(edicao_frame, text="Nova cultura:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        self.nova_cultura_var = tk.StringVar(value="")
        cultura_frame = ttk.Frame(edicao_frame)
        cultura_frame.grid(row=1, column=1, sticky=tk.W, padx=10, pady=5)
        ttk.Radiobutton(cultura_frame, text="Manter atual", variable=self.nova_cultura_var, value="").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(cultura_frame, text="Soja", variable=self.nova_cultura_var, value="0").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(cultura_frame, text="Milho", variable=self.nova_cultura_var, value="1").pack(side=tk.LEFT, padx=5)
        
        ttk.Label(edicao_frame, text="Novo comprimento (m):").grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        self.novo_comprimento_entry = ttk.Entry(edicao_frame, width=15)
        self.novo_comprimento_entry.grid(row=2, column=1, sticky=tk.W, padx=10, pady=5)
        
        ttk.Label(edicao_frame, text="Nova largura (m):").grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        self.nova_largura_entry = ttk.Entry(edicao_frame, width=15)
        self.nova_largura_entry.grid(row=3, column=1, sticky=tk.W, padx=10, pady=5)
        
        ttk.Button(edicao_frame, text="Atualizar", command=self.atualizar_lote).grid(row=4, column=0, columnspan=2, pady=15)
        
        ttk.Label(frame, text="Resultado da Atualização:").grid(row=2, column=0, sticky=tk.NW, padx=10, pady=5)
        self.resultado_atualizacao_text = scrolledtext.ScrolledText(frame, width=60, height=5, wrap=tk.WORD)
        self.resultado_atualizacao_text.grid(row=2, column=1, columnspan=2, sticky=tk.EW, padx=10, pady=5)
        self.resultado_atualizacao_text.config(state=tk.DISABLED)
        
        clima_frame = ttk.LabelFrame(frame, text="Clima Atual")
        clima_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky=tk.EW)
        
        ttk.Button(clima_frame, text="Buscar Dados Climáticos", command=self.buscar_dados_climaticos).grid(row=0, column=0, padx=5, pady=5)
        
        self.clima_atual_text = scrolledtext.ScrolledText(clima_frame, width=60, height=10, wrap=tk.WORD)
        self.clima_atual_text.grid(row=1, column=0, sticky=tk.EW, padx=10, pady=5)
        self.clima_atual_text.config(state=tk.DISABLED)
    
    def atualizar_lista_lotes(self, event=None):
        try:
            self.lotes_combobox.set('')
            
            opcoes = []
            for i, dado in enumerate(self.app.dados_salvos):
                opcoes.append(f"{i}: {dado['nome_lote']} ({calcular_area(dado['comprimento'], dado['largura'])} m²)")
            
            self.lotes_combobox['values'] = opcoes
            
            if opcoes:
                self.lotes_combobox.current(0) 
                self.carregar_dados_lote(None)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar lista de lotes: {str(e)}")
    
    def carregar_dados_lote(self, event):
        try:
            selecao = self.lotes_combobox.get()
            if not selecao:
                return
                
            indice = int(selecao.split(':')[0])
            self.indice_selecionado = indice
            
            if 0 <= indice < len(self.app.dados_salvos):
                dado = self.app.dados_salvos[indice]
                
                self.novo_nome_lote_entry.delete(0, tk.END)
                self.novo_nome_lote_entry.insert(0, dado['nome_lote'])
                
                self.nova_cultura_var.set("")
                
                self.novo_comprimento_entry.delete(0, tk.END)
                self.novo_comprimento_entry.insert(0, str(dado['comprimento']))
                
                self.nova_largura_entry.delete(0, tk.END)
                self.nova_largura_entry.insert(0, str(dado['largura']))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar dados do lote: {str(e)}")
    
    def atualizar_lote(self):
        try:
            if self.indice_selecionado is None:
                messagebox.showerror("Erro", "Nenhum lote selecionado.")
                return
                
            novo_nome = self.novo_nome_lote_entry.get()
            nova_cultura = self.nova_cultura_var.get()
            novo_comprimento = self.novo_comprimento_entry.get()
            nova_largura = self.nova_largura_entry.get()
            
            dado = self.app.dados_salvos[self.indice_selecionado]
            registro_id = dado["id"]
            
            if not novo_nome:
                novo_nome = dado["nome_lote"]
                
            cultura_final = int(nova_cultura) if nova_cultura else dado["cultura"]
            
            try:
                comprimento_final = int(novo_comprimento) if novo_comprimento else dado["comprimento"]
                largura_final = int(nova_largura) if nova_largura else dado["largura"]
            except ValueError:
                messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos para comprimento e largura.")
                return
                
            self.app.db_manager.atualizar_dados(registro_id, novo_nome, cultura_final, comprimento_final, largura_final)
            
            self.app.dados_salvos[self.indice_selecionado]["nome_lote"] = novo_nome
            self.app.dados_salvos[self.indice_selecionado]["cultura"] = cultura_final
            self.app.dados_salvos[self.indice_selecionado]["comprimento"] = comprimento_final
            self.app.dados_salvos[self.indice_selecionado]["largura"] = largura_final
            
            area = calcular_area(comprimento_final, largura_final)
            insumo_info = calcular_insumos(area, cultura_final)
            
            self.resultado_atualizacao_text.config(state=tk.NORMAL)
            self.resultado_atualizacao_text.delete(1.0, tk.END)
            
            resultado = f"Lote '{novo_nome}' atualizado com sucesso!\n"
            resultado += f"Cultura: {CULTURAS[cultura_final]}\n"
            resultado += f"Dimensões: {comprimento_final} m x {largura_final} m = {int(area)} m²\n"
            resultado += f"Insumo: {insumo_info['nome']}\n"
            resultado += f"Quantidade: {insumo_info['quantidade_total']/1000:.2f} L"
            
            self.resultado_atualizacao_text.insert(tk.END, resultado)
            self.resultado_atualizacao_text.config(state=tk.DISABLED)
            
            self.atualizar_lista_lotes()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar lote: {str(e)}")
    
    def exibir_clima_atual(self, dados):
        try:
            texto, self.dados_atuais_formatados = clima.formatar_dados_atuais(dados)
            
            self.clima_atual_text.config(state=tk.NORMAL)
            self.clima_atual_text.delete(1.0, tk.END)
            self.clima_atual_text.insert(tk.END, texto)
            self.clima_atual_text.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exibir clima atual: {str(e)}")
    
    def buscar_dados_climaticos(self):
        try:
            lat = self.app.latitude
            lon = self.app.longitude
            
            dados = clima.obter_dados_climaticos(lat, lon)
            if not dados:
                messagebox.showerror("Erro", "Não foi possível obter dados climáticos.")
                return
            
            self.exibir_clima_atual(dados)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar dados climáticos: {str(e)}")

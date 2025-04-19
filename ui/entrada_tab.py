import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

from utils import CULTURAS, calcular_area, calcular_insumos

class EntradaTab(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.configurar_aba()
    
    def configurar_aba(self):
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Welcome screen
        self.welcome_frame = ttk.Frame(self.main_frame)
        self.welcome_frame.pack(fill="both", expand=True)
        
        # Title with larger font
        title_label = ttk.Label(self.welcome_frame, text="FarmTech Solutions: Agricultura de Precisão", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=(30, 20))
        
        # Welcome text
        welcome_text = "Bem-vindo ao futuro da agricultura. Nossa plataforma oferece insights valiosos para maximizar a produtividade e a sustentabilidade de suas colheitas. Monitore e gerencie suas operações agrícolas com facilidade."
        message_label = ttk.Label(self.welcome_frame, text=welcome_text, wraplength=600, justify="center")
        message_label.pack(pady=20, padx=50)
        
        # Button to show input form
        btn_frame = ttk.Frame(self.welcome_frame)
        btn_frame.pack(pady=30)
        ttk.Button(btn_frame, text="Adicionar Dados", command=self.mostrar_formulario).pack()
        
        # Input form (initially hidden)
        self.form_frame = ttk.LabelFrame(self.main_frame, text="Entrada de Dados de Plantio")
        
        ttk.Label(self.form_frame, text="Nome do Talhão:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        self.nome_lote_entry = ttk.Entry(self.form_frame, width=40)
        self.nome_lote_entry.grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
        
        self.cultura_var = tk.StringVar(value="0")
        ttk.Label(self.form_frame, text="Cultura:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        cultura_frame = ttk.Frame(self.form_frame)
        cultura_frame.grid(row=1, column=1, sticky=tk.W, padx=10, pady=5)
        ttk.Radiobutton(cultura_frame, text="Soja", variable=self.cultura_var, value="0").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(cultura_frame, text="Milho", variable=self.cultura_var, value="1").pack(side=tk.LEFT, padx=5)
        
        ttk.Label(self.form_frame, text="Comprimento (m):").grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        self.comprimento_entry = ttk.Entry(self.form_frame, width=15)
        self.comprimento_entry.grid(row=2, column=1, sticky=tk.W, padx=10, pady=5)
        
        ttk.Label(self.form_frame, text="Largura (m):").grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        self.largura_entry = ttk.Entry(self.form_frame, width=15)
        self.largura_entry.grid(row=3, column=1, sticky=tk.W, padx=10, pady=5)
        
        form_btn_frame = ttk.Frame(self.form_frame)
        form_btn_frame.grid(row=4, column=0, columnspan=2, pady=15)
        
        ttk.Button(form_btn_frame, text="Processar e Salvar", command=self.processar_e_salvar).pack(side=tk.LEFT, padx=5)
        ttk.Button(form_btn_frame, text="Voltar", command=self.voltar_para_welcome).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(self.form_frame, text="Resultado:").grid(row=5, column=0, sticky=tk.NW, padx=10, pady=5)
        self.resultado_text = scrolledtext.ScrolledText(self.form_frame, width=60, height=10, wrap=tk.WORD)
        self.resultado_text.grid(row=5, column=1, sticky=tk.EW, padx=10, pady=5)
        self.resultado_text.config(state=tk.DISABLED)
    
    def mostrar_formulario(self):
        self.welcome_frame.pack_forget()
        self.form_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    def voltar_para_welcome(self):
        self.form_frame.pack_forget()
        self.welcome_frame.pack(fill="both", expand=True)
        
    def processar(self):
        self.processar_e_salvar()
    
    def processar_e_salvar(self):
        nome_lote = self.nome_lote_entry.get()
        cultura = self.cultura_var.get()
        comprimento = self.comprimento_entry.get()
        largura = self.largura_entry.get()
        
        if not nome_lote or not comprimento or not largura:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
            return
        
        try:
            comprimento = int(comprimento)
            largura = int(largura)
            cultura = int(cultura)
            
            area = calcular_area(comprimento, largura)
            insumo_info = calcular_insumos(area, cultura)
            
            resultado = f"Lote: {nome_lote}\n"
            resultado += f"Cultura: {CULTURAS[cultura]}\n"
            resultado += f"Dimensões: {comprimento} m x {largura} m = {int(area)} m²\n"
            resultado += f"Insumo: {insumo_info['nome']}\n"
            resultado += f"Taxa de aplicação: {insumo_info['taxa']} mL/m²\n"
            resultado += f"Quantidade total: {insumo_info['quantidade_total']/1000:.2f} L de {insumo_info['nome']}"
            
            self.resultado_text.config(state=tk.NORMAL)
            self.resultado_text.delete(1.0, tk.END)
            self.resultado_text.insert(tk.END, resultado)
            self.resultado_text.config(state=tk.DISABLED)
            
            novo_dado = self.app.db_manager.salvar_dados(nome_lote, cultura, comprimento, largura)
            
            self.app.dados_salvos.append(novo_dado)
            
            self.app.tab_dados.listar_dados(self.app.dados_salvos)
            
            messagebox.showinfo("Sucesso", "Dados processados e salvos com sucesso!")
            
            self.nome_lote_entry.delete(0, tk.END)
            self.comprimento_entry.delete(0, tk.END)
            self.largura_entry.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos para comprimento e largura.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao processar e salvar dados: {str(e)}")
            
    def salvar(self):
        self.processar_e_salvar()

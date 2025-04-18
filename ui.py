import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext


from subalgoritmos.db import DatabaseManager
import subalgoritmos.clima as clima
import subalgoritmos.analise as analise

CULTURAS = {0: "Soja", 1: "Milho"}


def calcular_area(comprimento, largura):
    return comprimento * largura

def calcular_insumos(area, cultura):
    insumos_por_cultura = {
    0: {"nome": "Glifosato", "taxa": 1200, "descrição": "Herbicida para controle de ervas daninhas"},
    1: {"nome": "NPK 20-10-10", "taxa": 200, "descrição": "Fertilizante para desenvolvimento da planta"}
    }
    insumo_info = insumos_por_cultura[cultura]
    quantidade = area * insumo_info["taxa"]
    
    return {
        "nome": insumo_info["nome"],
        "taxa": insumo_info["taxa"],
        "quantidade_total": quantidade
    }

class FarmTechApp(tk.Tk):
    def __init__(self):
        super().__init__()
        

        self.title("FarmTech Solutions - Monitoramento Agrícola")
        self.geometry("1000x700")
        self.configure(bg="#f0f0f0")
        

        self.dados_salvos = []
        

        self.db_path = "farmtech_solutions.sqlite"
        self.db_manager = DatabaseManager(self.db_path)
        self.carregar_dados()
        

        self.latitude = -30.0277
        self.longitude = -51.2287
        

        self.criar_interface()
        

        self.after(100, self.inicializar_interface)
    

    
    def carregar_dados(self):
        try:
            self.dados_salvos = self.db_manager.carregar_dados()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar dados: {str(e)}")
    
    def salvar_dados_arquivo(self):
        pass
    

    
    def criar_interface(self):
        
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        

        self.tab_entrada = ttk.Frame(self.notebook)
        self.tab_dados = ttk.Frame(self.notebook)
        self.tab_clima = ttk.Frame(self.notebook)
        self.tab_analise = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_entrada, text="Entrada de Dados")
        self.notebook.add(self.tab_dados, text="Dados")
        self.notebook.add(self.tab_clima, text="Dados Climáticos")
        self.notebook.add(self.tab_analise, text="Análise de Impacto")
        

        self.configurar_aba_entrada()
        self.configurar_aba_dados()
        self.configurar_aba_clima()
        self.configurar_aba_analise()

    def configurar_aba_entrada(self):
        frame = ttk.LabelFrame(self.tab_entrada, text="Entrada de Dados de Plantio")
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        

        ttk.Label(frame, text="Nome do Talhão:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        self.nome_lote_entry = ttk.Entry(frame, width=40)
        self.nome_lote_entry.grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
        

        self.cultura_var = tk.StringVar(value="0")
        ttk.Label(frame, text="Cultura:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        cultura_frame = ttk.Frame(frame)
        cultura_frame.grid(row=1, column=1, sticky=tk.W, padx=10, pady=5)
        ttk.Radiobutton(cultura_frame, text="Soja", variable=self.cultura_var, value="0").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(cultura_frame, text="Milho", variable=self.cultura_var, value="1").pack(side=tk.LEFT, padx=5)
        
        ttk.Label(frame, text="Comprimento (m):").grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        self.comprimento_entry = ttk.Entry(frame, width=15)
        self.comprimento_entry.grid(row=2, column=1, sticky=tk.W, padx=10, pady=5)
        
        ttk.Label(frame, text="Largura (m):").grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        self.largura_entry = ttk.Entry(frame, width=15)
        self.largura_entry.grid(row=3, column=1, sticky=tk.W, padx=10, pady=5)
        

        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=15)
        
        ttk.Button(btn_frame, text="Processar e Salvar", command=self.processar_e_salvar).pack(side=tk.LEFT, padx=5)
        

        ttk.Label(frame, text="Resultado:").grid(row=5, column=0, sticky=tk.NW, padx=10, pady=5)
        self.resultado_text = scrolledtext.ScrolledText(frame, width=60, height=10, wrap=tk.WORD)
        self.resultado_text.grid(row=5, column=1, sticky=tk.EW, padx=10, pady=5)
        self.resultado_text.config(state=tk.DISABLED)
    
    def configurar_aba_dados(self):
        main_frame = ttk.Frame(self.tab_dados)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        

        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill="x", expand=False, pady=10)
        
        ttk.Button(top_frame, text="Atualizar Tabela", command=self.listar_dados).pack(side=tk.LEFT, padx=5)
        

        table_frame = ttk.LabelFrame(main_frame, text="Dados Cadastrados")
        table_frame.pack(fill="both", expand=True, padx=5, pady=5)
        

        tree_frame = ttk.Frame(table_frame)
        tree_frame.pack(fill="both", expand=True, padx=5, pady=5)
        

        colunas = ("nome", "cultura", "comprimento", "largura", "area", "insumo", "taxa", "quantidade", "acoes")
        self.tabela = ttk.Treeview(tree_frame, columns=colunas, show="headings", height=15)
        
        self.tabela.heading("nome", text="Nome do Lote")
        self.tabela.heading("cultura", text="Cultura")
        self.tabela.heading("comprimento", text="Comprimento (m)")
        self.tabela.heading("largura", text="Largura (m)")
        self.tabela.heading("area", text="Área (m²)")
        self.tabela.heading("insumo", text="Insumo")
        self.tabela.heading("taxa", text="Taxa")
        self.tabela.heading("quantidade", text="Quantidade Total")
        self.tabela.heading("acoes", text="Ações")
        
        self.tabela.column("nome", width=150)
        self.tabela.column("cultura", width=80)
        self.tabela.column("comprimento", width=80)
        self.tabela.column("largura", width=80)
        self.tabela.column("area", width=80)
        self.tabela.column("insumo", width=100)
        self.tabela.column("taxa", width=80)
        self.tabela.column("quantidade", width=100)
        self.tabela.column("acoes", width=120)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tabela.yview)
        self.tabela.configure(yscroll=scrollbar.set)
        
        self.tabela.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        

        self.edicao_frame = ttk.LabelFrame(main_frame, text="Editar Item")
        self.edicao_frame.pack(fill="x", expand=False, padx=5, pady=10)
        

        edit_fields_frame = ttk.Frame(self.edicao_frame)
        edit_fields_frame.pack(fill="x", expand=True, padx=10, pady=10)
        

        ttk.Label(edit_fields_frame, text="Nome do lote:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.edit_nome_lote_entry = ttk.Entry(edit_fields_frame, width=30)
        self.edit_nome_lote_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        

        ttk.Label(edit_fields_frame, text="Cultura:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.edit_cultura_var = tk.StringVar()
        cultura_frame = ttk.Frame(edit_fields_frame)
        cultura_frame.grid(row=0, column=3, sticky=tk.W, padx=5, pady=5)
        ttk.Radiobutton(cultura_frame, text="Soja", variable=self.edit_cultura_var, value="0").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(cultura_frame, text="Milho", variable=self.edit_cultura_var, value="1").pack(side=tk.LEFT, padx=5)
        

        ttk.Label(edit_fields_frame, text="Comprimento (m):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.edit_comprimento_entry = ttk.Entry(edit_fields_frame, width=10)
        self.edit_comprimento_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        

        ttk.Label(edit_fields_frame, text="Largura (m):").grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        self.edit_largura_entry = ttk.Entry(edit_fields_frame, width=10)
        self.edit_largura_entry.grid(row=1, column=3, sticky=tk.W, padx=5, pady=5)
        

        buttons_frame = ttk.Frame(self.edicao_frame)
        buttons_frame.pack(fill="x", expand=True, padx=10, pady=10)
        
        self.salvar_edicao_btn = ttk.Button(buttons_frame, text="Salvar Alterações", command=self.salvar_edicao, state=tk.DISABLED)
        self.salvar_edicao_btn.pack(side=tk.LEFT, padx=5)
        
        self.cancelar_edicao_btn = ttk.Button(buttons_frame, text="Cancelar", command=self.cancelar_edicao, state=tk.DISABLED)
        self.cancelar_edicao_btn.pack(side=tk.LEFT, padx=5)
        

        self.item_em_edicao = None
        

        self.edicao_frame.pack_forget()
    
    def configurar_aba_clima(self):
        frame = ttk.LabelFrame(self.tab_clima, text="Dados Climáticos")

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
        

        self.indice_selecionado = None
    

        
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
            

            novo_dado = self.db_manager.salvar_dados(nome_lote, cultura, comprimento, largura)
            

            self.dados_salvos.append(novo_dado)
            

            self.listar_dados()
            

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
    
    def listar_dados(self):

        for item in self.tabela.get_children():
            self.tabela.delete(item)
        
        if not self.dados_salvos:
            messagebox.showinfo("Informação", "Nenhum dado cadastrado.")
            return
        

        for i, dado in enumerate(self.dados_salvos):
            nome_lote = dado["nome_lote"]
            cultura_idx = dado["cultura"]
            comp = dado["comprimento"]
            larg = dado["largura"]
            area = calcular_area(comp, larg)
            insumo_info = calcular_insumos(area, cultura_idx)
            
            cultura_nome = "Soja" if cultura_idx == 0 else "Milho"
            

            item_id = self.tabela.insert("", "end", values=(
                nome_lote,
                cultura_nome,
                f"{comp} m",
                f"{larg} m",
                f"{int(area)} m²",
                insumo_info['nome'],
                f"{insumo_info['taxa']} mL/m²",
                f"{insumo_info['quantidade_total']/1000:.2f} L",
                "Ações"
            ))
            

            self.tabela.tag_bind(item_id, '<Double-1>', lambda event, idx=i: self.iniciar_edicao(idx))
        

        self.adicionar_botoes_acoes()
    
    def atualizar_lista_lotes(self, event=None):
        try:
            self.lotes_combobox.set('')
            
            opcoes = []
            for i, dado in enumerate(self.dados_salvos):
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
            
            if 0 <= indice < len(self.dados_salvos):
                dado = self.dados_salvos[indice]
                
                self.novo_nome_lote_entry.delete(0, tk.END)
                self.novo_nome_lote_entry.insert(0, dado['nome_lote'])
                
                self.nova_cultura_var.set("")
                
                self.novo_comprimento_entry.delete(0, tk.END)
                self.novo_comprimento_entry.insert(0, str(dado['comprimento']))
                
                self.nova_largura_entry.delete(0, tk.END)
                self.nova_largura_entry.insert(0, str(dado['largura']))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar dados do lote: {str(e)}")
    
    def atualizar_lista_lotes_deletar(self, event=None):
        try:
            self.lotes_deletar_combobox.set('')
            
            opcoes = []
            for i, dado in enumerate(self.dados_salvos):
                opcoes.append(f"{i}: {dado['nome_lote']} ({calcular_area(dado['comprimento'], dado['largura'])} m²)")
            
            self.lotes_deletar_combobox['values'] = opcoes
            
            self.lotes_deletar_combobox.bind("<<ComboboxSelected>>", self.mostrar_info_lote)
            
            if opcoes:
                self.lotes_deletar_combobox.current(0) 
                self.mostrar_info_lote(None)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar lista de lotes: {str(e)}")
    
    def mostrar_info_lote(self, event):
        try:
            selecao = self.lotes_deletar_combobox.get()
            if not selecao:
                return
                
            indice = int(selecao.split(':')[0])
            self.indice_deletar_selecionado = indice
            
            if 0 <= indice < len(self.dados_salvos):
                dado = self.dados_salvos[indice]
                
                self.info_lote_text.config(state=tk.NORMAL)
                self.info_lote_text.delete(1.0, tk.END)
                
                cultura = "Soja" if dado['cultura'] == 0 else "Milho"
                area = calcular_area(dado['comprimento'], dado['largura'])
                insumo_info = calcular_insumos(area, dado['cultura'])
                
                info = f"Nome do Lote: {dado['nome_lote']}\n"
                info += f"Cultura: {cultura}\n"
                info += f"Comprimento: {dado['comprimento']} m\n"
                info += f"Largura: {dado['largura']} m\n"
                info += f"\u00c1rea: {area} m\u00b2\n"
                info += f"Insumo: {insumo_info['nome']}\n"
                info += f"Taxa: {insumo_info['taxa']} mL/m\u00b2\n"
                info += f"Quantidade Total: {insumo_info['quantidade_total']/1000:.2f} L"
                
                self.info_lote_text.insert(tk.END, info)
                self.info_lote_text.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao mostrar informações do lote: {str(e)}")
            
    def adicionar_botoes_acoes(self):
        self.tabela.bind("<Double-1>", self.on_tabela_double_click)
        
        for i, item_id in enumerate(self.tabela.get_children()):
            self.tabela.set(item_id, "acoes", "Editar / Deletar")
    
    def on_tabela_double_click(self, event):
        item_id = self.tabela.identify_row(event.y)
        if not item_id:
            return
            
        coluna = self.tabela.identify_column(event.x)
        coluna_idx = int(coluna.replace('#', '')) - 1
        
        indice = self.tabela.index(item_id)
        
        if coluna_idx == 8:
            self.mostrar_menu_acoes(event, indice)
        else:
            self.iniciar_edicao(indice)
    
    def mostrar_menu_acoes(self, event, indice):
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Editar", command=lambda: self.iniciar_edicao(indice))
        menu.add_command(label="Deletar", command=lambda: self.confirmar_delecao(indice))
        menu.tk_popup(event.x_root, event.y_root)
    
    def iniciar_edicao(self, indice):
        if indice < 0 or indice >= len(self.dados_salvos):
            return
            
        self.edicao_frame.pack(fill="x", expand=False, padx=5, pady=10)
        
        dado = self.dados_salvos[indice]
        
        self.edit_nome_lote_entry.delete(0, tk.END)
        self.edit_nome_lote_entry.insert(0, dado['nome_lote'])
        
        self.edit_cultura_var.set(str(dado['cultura']))
        
        self.edit_comprimento_entry.delete(0, tk.END)
        self.edit_comprimento_entry.insert(0, str(dado['comprimento']))
        
        self.edit_largura_entry.delete(0, tk.END)
        self.edit_largura_entry.insert(0, str(dado['largura']))
        
        self.item_em_edicao = indice
        
        self.salvar_edicao_btn.config(state=tk.NORMAL)
        self.cancelar_edicao_btn.config(state=tk.NORMAL)
    
    def cancelar_edicao(self):
        self.edicao_frame.pack_forget()
        
        self.edit_nome_lote_entry.delete(0, tk.END)
        self.edit_cultura_var.set("")
        self.edit_comprimento_entry.delete(0, tk.END)
        self.edit_largura_entry.delete(0, tk.END)
        
        self.item_em_edicao = None
        
        self.salvar_edicao_btn.config(state=tk.DISABLED)
        self.cancelar_edicao_btn.config(state=tk.DISABLED)
    
    def salvar_edicao(self):
        if self.item_em_edicao is None:
            return
            
        novo_nome = self.edit_nome_lote_entry.get()
        nova_cultura = self.edit_cultura_var.get()
        novo_comprimento = self.edit_comprimento_entry.get()
        nova_largura = self.edit_largura_entry.get()
        
        try:
            registro_id = self.dados_salvos[self.item_em_edicao]["id"]
            
            if not novo_nome or not nova_cultura or not novo_comprimento or not nova_largura:
                messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
                return
                

            cultura_final = int(nova_cultura)
            comprimento_final = int(novo_comprimento)
            largura_final = int(nova_largura)
            
            self.db_manager.atualizar_dados(registro_id, novo_nome, cultura_final, comprimento_final, largura_final)
            
            self.dados_salvos[self.item_em_edicao]["nome_lote"] = novo_nome
            self.dados_salvos[self.item_em_edicao]["cultura"] = cultura_final
            self.dados_salvos[self.item_em_edicao]["comprimento"] = comprimento_final
            self.dados_salvos[self.item_em_edicao]["largura"] = largura_final
            

            self.listar_dados()
            

            self.cancelar_edicao()
            

            messagebox.showinfo("Sucesso", f"Lote '{novo_nome}' atualizado com sucesso!")
            
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos para comprimento e largura.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar dados: {str(e)}")
    
    def confirmar_delecao(self, indice):
        if indice < 0 or indice >= len(self.dados_salvos):
            return
            
        dado = self.dados_salvos[indice]
        nome_lote = dado["nome_lote"]
        

        if messagebox.askyesno("Confirmar Deleção", f"Tem certeza que deseja deletar o lote '{nome_lote}'?"):
            self.deletar_item(indice)
    
    def deletar_item(self, indice):
        try:

            registro_id = self.dados_salvos[indice]["id"]
            nome_lote = self.dados_salvos[indice]["nome_lote"]
            

            self.db_manager.deletar_dados(registro_id)
            

            del self.dados_salvos[indice]
            

            self.listar_dados()
            

            messagebox.showinfo("Sucesso", f"Lote '{nome_lote}' deletado com sucesso!")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao deletar dados: {str(e)}")
    
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

            lat = self.latitude
            lon = self.longitude
            

            dados = clima.obter_dados_climaticos(lat, lon)
            if not dados:
                messagebox.showerror("Erro", "Não foi possível obter dados climáticos.")
                return
            

            self.exibir_clima_atual(dados)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar dados climáticos: {str(e)}")



        
    def realizar_analise_impacto(self):
        try:
            cultura_id = int(self.analise_cultura_var.get())
            cultura_nome = CULTURAS[cultura_id]
            

            dados = clima.obter_dados_climaticos(self.latitude, self.longitude)
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
    

    def atualizar_lote(self):
        try:
            if self.indice_selecionado is None:
                messagebox.showerror("Erro", "Nenhum lote selecionado.")
                return
                
            novo_nome = self.novo_nome_lote_entry.get()
            nova_cultura = self.nova_cultura_var.get()
            novo_comprimento = self.novo_comprimento_entry.get()
            nova_largura = self.nova_largura_entry.get()
            
            dado = self.dados_salvos[self.indice_selecionado]
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
                
            self.db_manager.atualizar_dados(registro_id, novo_nome, cultura_final, comprimento_final, largura_final)
            
            self.dados_salvos[self.indice_selecionado]["nome_lote"] = novo_nome
            self.dados_salvos[self.indice_selecionado]["cultura"] = cultura_final
            self.dados_salvos[self.indice_selecionado]["comprimento"] = comprimento_final
            self.dados_salvos[self.indice_selecionado]["largura"] = largura_final
            
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
    
    def configurar_aba_analise(self):
        frame = ttk.LabelFrame(self.tab_analise, text="Análise de Impacto Climático")
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
    
    def inicializar_interface(self):
        self.listar_dados()
        self.buscar_dados_climaticos()


if __name__ == "__main__":
    print("Iniciando interface FarmTech Solutions - Rio Grande do Sul...")
    app = FarmTechApp()
    app.mainloop()

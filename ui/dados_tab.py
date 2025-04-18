import tkinter as tk
from tkinter import ttk, messagebox

from utils import CULTURAS, calcular_area, calcular_insumos

class DadosTab(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.item_em_edicao = None
        self.configurar_aba()
    
    def configurar_aba(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill="x", expand=False, pady=10)
        
        ttk.Button(top_frame, text="Atualizar Tabela", command=self.atualizar_tabela).pack(side=tk.LEFT, padx=5)
        
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
        
        self.edicao_frame.pack_forget()
    
    def atualizar_dados(self, dados):
        self.app.dados_salvos = dados
    
    def atualizar_tabela(self):
        self.listar_dados(self.app.dados_salvos)
    
    def listar_dados(self, dados=None):
        if dados is None:
            dados = self.app.dados_salvos
            
        for item in self.tabela.get_children():
            self.tabela.delete(item)
        
        if not dados:
            messagebox.showinfo("Informação", "Nenhum dado cadastrado.")
            return
        
        for i, dado in enumerate(dados):
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
        if indice < 0 or indice >= len(self.app.dados_salvos):
            return
            
        self.edicao_frame.pack(fill="x", expand=False, padx=5, pady=10)
        
        dado = self.app.dados_salvos[indice]
        
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
            registro_id = self.app.dados_salvos[self.item_em_edicao]["id"]
            
            if not novo_nome or not nova_cultura or not novo_comprimento or not nova_largura:
                messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
                return
                
            cultura_final = int(nova_cultura)
            comprimento_final = int(novo_comprimento)
            largura_final = int(nova_largura)
            
            self.app.db_manager.atualizar_dados(registro_id, novo_nome, cultura_final, comprimento_final, largura_final)
            
            self.app.dados_salvos[self.item_em_edicao]["nome_lote"] = novo_nome
            self.app.dados_salvos[self.item_em_edicao]["cultura"] = cultura_final
            self.app.dados_salvos[self.item_em_edicao]["comprimento"] = comprimento_final
            self.app.dados_salvos[self.item_em_edicao]["largura"] = largura_final
            
            self.listar_dados()
            
            self.cancelar_edicao()
            
            messagebox.showinfo("Sucesso", f"Lote '{novo_nome}' atualizado com sucesso!")
            
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos para comprimento e largura.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar dados: {str(e)}")
    
    def confirmar_delecao(self, indice):
        if indice < 0 or indice >= len(self.app.dados_salvos):
            return
            
        dado = self.app.dados_salvos[indice]
        nome_lote = dado["nome_lote"]
        
        if messagebox.askyesno("Confirmar Deleção", f"Tem certeza que deseja deletar o lote '{nome_lote}'?"):
            self.deletar_item(indice)
    
    def deletar_item(self, indice):
        try:
            registro_id = self.app.dados_salvos[indice]["id"]
            nome_lote = self.app.dados_salvos[indice]["nome_lote"]
            
            self.app.db_manager.deletar_dados(registro_id)
            
            del self.app.dados_salvos[indice]
            
            self.listar_dados()
            
            messagebox.showinfo("Sucesso", f"Lote '{nome_lote}' deletado com sucesso!")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao deletar dados: {str(e)}")

# Importações
from customtkinter import *
from conexao import criar_tabelas
from services import *
from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from datetime import datetime

# Função para abrir a janela de edição de uma despesa
def abrir_editar_janela():
    item_selecionado = tree.selection()
    if not item_selecionado:
        messagebox.showwarning("Aviso", "Selecione uma despesa para editar.")
        return
    despesa_id = tree.item(item_selecionado[0])['values'][0]
    valor, categoria, data, descricao = tree.item(item_selecionado[0])['values'][1:]

    # Janela de edição
    edit_janela = Toplevel(janela)
    edit_janela.title("Editar Despesa")
    edit_janela.geometry("300x300")
    edit_janela.configure(bg='#202021')
    edit_janela.transient(janela)  # Define a janela principal como background
    edit_janela.grab_set()  # Mantém o foco nesta janela

    # Campos de edição
    CTkLabel(edit_janela, text="Valor:", font=('Helvetica', 14), text_color="white").pack(pady=5)
    valorEntr_edit = CTkEntry(edit_janela, width=200)
    valorEntr_edit.insert(0, valor)
    valorEntr_edit.pack()

    CTkLabel(edit_janela, text="Categoria:", font=('Helvetica', 14), text_color="white").pack(pady=5)
    categoriaEntr_edit = CTkEntry(edit_janela, width=200)
    categoriaEntr_edit.insert(0, categoria)
    categoriaEntr_edit.pack()

    CTkLabel(edit_janela, text="Data (AAAA-MM-DD):", font=('Helvetica', 14), text_color="white").pack(pady=5)
    dataEntr_edit = CTkEntry(edit_janela, width=200)
    dataEntr_edit.insert(0, data)
    dataEntr_edit.pack()

    CTkLabel(edit_janela, text="Descrição:", font=('Helvetica', 14), text_color="white").pack(pady=5)
    descEntr_edit = CTkEntry(edit_janela, width=200)
    descEntr_edit.insert(0, descricao)
    descEntr_edit.pack()

    # Botão para salvar alterações
    CTkButton(edit_janela, text="Salvar Alterações", command=lambda: salvar_edicao(despesa_id, valorEntr_edit, categoriaEntr_edit, dataEntr_edit, descEntr_edit, edit_janela)).pack(pady=10)

# Função para salvar as edições feitas na despesa
def salvar_edicao(despesa_id, valor_entry, categoria_entry, data_entry, desc_entry, janela_edicao):
    try:
        valor = float(valor_entry.get())
        categoria = categoria_entry.get().strip()
        data = datetime.strptime(data_entry.get(), '%Y-%m-%d').date()
        descricao = desc_entry.get().strip()
        atualizar_despesa(despesa_id, valor, categoria, data, descricao)
        janela_edicao.destroy()
        listar_despesas()
    except ValueError:
        messagebox.showerror("Erro", "Informe um valor numérico válido e data no formato AAAA-MM-DD.")

# Função para abrir a janela de despesas
def abrir_despesas_janela():
    global tree
    # Janela de despesas
    despesas_janela = CTkToplevel(janela)
    despesas_janela.title("Tabela de Despesas")
    despesas_janela.geometry("800x500")
    despesas_janela.configure(background='#202021')
    despesas_janela.transient(janela)
    despesas_janela.resizable(False, False)
    despesas_janela.grab_set()
    centralizar_janela(despesas_janela, largura=800, altura=500)

    # Frame da tabela
    frame_tree = CTkFrame(despesas_janela)
    frame_tree.pack(fill="both", expand=True, padx=20, pady=20)

    # Barra de pesquisa
    pesquisa_frame = CTkFrame(despesas_janela)
    pesquisa_frame.pack(pady=10)

    search_label = CTkLabel(pesquisa_frame, text="Pesquisar:", font=('Helvetica', 14), text_color="white")
    search_label.grid(row=0, column=0, padx=5, pady=5)
    search_entry = CTkEntry(pesquisa_frame, width=200, placeholder_text="Digite sua pesquisa...")
    search_entry.grid(row=0, column=1, padx=5, pady=5)

    # Função para listar despesas na tabela
    def listar_despesas_tabela():
        tree.delete(*tree.get_children())
        for despesa in listar_despesas():
            tree.insert('', 'end', values=despesa)

    # Função para pesquisa de despesas que pode exibir por categoria
    def pesquisar_despesas():
        query = search_entry.get().strip().lower()
        tree.delete(*tree.get_children())
        for despesa in listar_despesas():
            if any(query in str(campo).lower() for campo in despesa):
                tree.insert('', 'end', values=despesa)

    # Botão de pesquisa
    pesquisarBotao = CTkButton(pesquisa_frame, text="Pesquisar", command=pesquisar_despesas)
    pesquisarBotao.grid(row=0, column=2, padx=5, pady=5)

    # Estilo da tabela
    style = ttk.Style()
    style.theme_use("alt")
    style.configure("Treeview", background="black", fieldbackground="black", foreground="gray")

    # Configuração da tabela de despesas
    tree = ttk.Treeview(frame_tree, columns=('ID', 'Valor', 'Categoria', 'Data', 'Descrição'), show='headings', height=12)
    tree.heading('ID', text='ID')
    tree.heading('Valor', text='Valor')
    tree.heading('Categoria', text='Categoria')
    tree.heading('Data', text='Data')
    tree.heading('Descrição', text='Descrição')

    # Ajuste de colunas
    tree.column('ID', width=50)
    tree.column('Valor', width=100)
    tree.column('Categoria', width=150)
    tree.column('Data', width=100)
    tree.column('Descrição', width=250)
    tree.pack(fill="both", expand=True, padx=20, pady=10)

    # Carregar despesas na tabela
    listar_despesas_tabela()

    # Função para remover despesa selecionada
    def acao_remover():
        item_selecionado = tree.selection()
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Selecione uma despesa para remover.")
            return
        despesa_id = tree.item(item_selecionado[0])['values'][0]
        resposta = messagebox.askyesno("Confirmação", "Tem certeza que deseja remover a despesa?")
        if resposta:
            remover_despesa(despesa_id)
            listar_despesas_tabela()
            atualizar_total()

    # Botão de Remover Despesa
    remover_button = CTkButton(despesas_janela, text="Remover Despesa", command=acao_remover)
    remover_button.pack(side="left", padx=20, pady=10)

    # Botão de Editar Despesa
    editar_button = CTkButton(despesas_janela, text="Editar Despesa", command=abrir_editar_janela)
    editar_button.pack(side="left", padx=20, pady=10)

    # Botão de Voltar para o Menu Principal
    voltar_button = CTkButton(despesas_janela, text="Voltar", command=despesas_janela.destroy)
    voltar_button.pack(side="right", padx=20, pady=10)

# Funções de adicionar e atualizar totais na GUI
def adicionar_despesas():
    try:
        valor = float(valorEntr.get())
        categoria = categoriaEntr.get().strip()
        data = datetime.strptime(dataEntr.get(), '%Y-%m-%d').date()
        descricao = descEntr.get().strip()
        
        if any(not campo for campo in [valor, categoria, data, descricao]):
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return
        if valor <= 0:
            raise ValueError("Valor inválido.")

        inserir_despesa(valor, categoria, data, descricao)
        valorEntr.delete(0, END)
        categoriaEntr.delete(0, END)
        dataEntr.delete(0, END)
        descEntr.delete(0, END)
        atualizar_total()
    except ValueError:
        messagebox.showerror("Erro", "Informe um valor numérico válido para a despesa e data no formato AAAA-MM-DD.")

def atualizar_total():
    despesas = listar_despesas()
    total_mes = sum(d[1] for d in despesas)
    media_diaria = total_mes / 30 if total_mes > 0 else 0
    totalLabel.configure(text=f"Total de despesas mensais: R${total_mes:.2f}")
    mediaLabel.configure(text=f"Média Diária: R${media_diaria:.2f}")

# Configuração da janela principal e inicialização
janela = CTk()
janela.geometry("450x480")
janela.title("Gerenciador de Despesas")
janela.resizable(False, False)
set_appearance_mode("dark")
set_default_color_theme("dark-blue")

# Função para centralizar a janela
def centralizar_janela(janela, largura=450, altura=480):
    alt_tela = janela.winfo_screenheight()
    larg_tela = janela.winfo_screenwidth()
    x = (larg_tela - largura) // 2
    y = (alt_tela - altura) // 2
    janela.geometry(f"{largura}x{altura}+{x}+{y}")

centralizar_janela(janela, largura=450, altura=480)

# Layout principal
frame_principal = CTkFrame(janela)
frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
titulo = CTkLabel(frame_principal, text="Gerenciador de Despesas", font=('Helvetica', 24, 'bold'))
titulo.pack(pady=10)

# Formulário de entrada
frame_form = CTkFrame(frame_principal)
frame_form.pack(pady=10)
CTkLabel(frame_form, text="Valor:", font=('Helvetica', 14)).grid(row=0, column=0, padx=5, pady=5, sticky='e')
valorEntr = CTkEntry(frame_form, width=200)
valorEntr.grid(row=0, column=1)
CTkLabel(frame_form, text="Categoria:", font=('Helvetica', 14)).grid(row=1, column=0, padx=5, pady=5, sticky='e')
categoriaEntr = CTkEntry(frame_form, width=200)
categoriaEntr.grid(row=1, column=1)
CTkLabel(frame_form, text="Data (AAAA-MM-DD):", font=('Helvetica', 14)).grid(row=2, column=0, padx=5, pady=5, sticky='e')
dataEntr = CTkEntry(frame_form, width=200)
dataEntr.grid(row=2, column=1)
CTkLabel(frame_form, text="Descrição:", font=('Helvetica', 14)).grid(row=3, column=0, padx=5, pady=5, sticky='e')
descEntr = CTkEntry(frame_form, width=200)
descEntr.grid(row=3, column=1)

# Botões principais
CTkButton(frame_principal, text="Adicionar Despesa", command=adicionar_despesas).pack(pady=10)
CTkButton(frame_principal, text="Listar Despesas", command=abrir_despesas_janela).pack()

# Labels de totais
totalLabel = CTkLabel(frame_principal, text="Total de despesas mensais: R$0.00", font=('Helvetica', 14, 'bold'))
totalLabel.pack(pady=10)
mediaLabel = CTkLabel(frame_principal, text="Média Diária: R$0.00", font=('Helvetica', 14, 'bold'))
mediaLabel.pack()

# Logo do grupo
try:
    img = Image.open("task.png")  
    img = img.resize((55, 55), Image.LANCZOS)  
    imgtk = ImageTk.PhotoImage(img)
    label_imagem = Label(janela, image=imgtk, bg="#202120")  
    label_imagem.image = imgtk  
    label_imagem.place(x=370, y=400)
except FileNotFoundError:
    messagebox.showwarning("Aviso", "Logo não encontrado. Certifique-se de que o arquivo 'taskforce_logo.png' está no diretório correto.")

# Inicialização
criar_tabelas()
atualizar_total()
janela.mainloop()
from cryptography.fernet import Fernet
from pymongo import MongoClient
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import ttk

# ==== CONEXÃO COM BANCO E CRIPTOGRAFIA ====
key = b'AD5BIGDLa34gtAtmKkVSI_c4pHGPOizinaA5Ya-k2Mw='
fernet = Fernet(key)

try:
    doces = MongoClient("mongodb+srv://123:123@meubanco.apcmzzs.mongodb.net/?retryWrites=true&w=majority&appName=meubanco")
    doces.admin.command('ping') 
    collection = doces["CofredeDoces"]["Registros"]
    DB_CONNECTED = True
except Exception as e:
    print(f"ERRO DE CONEXÃO COM O MONGODB: {e}")
    DB_CONNECTED = False
    collection = None

# ==== JANELA PRINCIPAL ====
janela = Tk()
janela.title('🍬 Cofre de Doces 🍭')
janela.state('zoomed')
janela.configure(bg="white")

# Variáveis globais para os widgets (necessárias para o modo de troca de telas)
entry_nome = None
entry_tipo = None
entry_qtd = None
entry_data = None
entry_list_tipo = None
list_tree = None
decrypt_tree = None

# ==== IMAGEM DE FUNDO ====
try:
    imagem_fundo = Image.open(r"C:\Users\Nicollas de Souza\OneDrive\Documentos\projeto Bruno 4 bim\projeto1.jpg")
    imagem = imagem_fundo.resize((200, 200))
    img_tk = ImageTk.PhotoImage(imagem)
except FileNotFoundError:
    img_tk = None

# ==== FUNÇÃO AUXILIAR PARA LIMPAR A JANELA ====
def limpar_janela():
    """Remove todos os widgets da janela principal."""
    for widget in janela.winfo_children():
        widget.destroy()

# ==========================
# ==== TELAS DA APLICAÇÃO ====
# ==========================

def desenhar_tela_principal():
    """Desenha a tela inicial com o título e os botões de navegação."""
    limpar_janela()

    # Imagens de Fundo
    if img_tk:
        Limg = Label(janela, image=img_tk, bg="white")
        Limg.place(x=0, y=0)
        Rimg = Label(janela, image=img_tk, bg="white")
        Rimg.place(relx=1.0, rely=0, x=-45, y=0, anchor='ne')

        # === 2. MEIO D/E (NOVAS) ===
        # rely=0.45 coloca a imagem aproximadamente no meio da janela
        Limg_mid = Label(janela, image=img_tk, bg="white")
        Limg_mid.place(x=0, y=-90, rely=0.45)  # Lateral esquerda, meio
        Rimg_mid = Label(janela, image=img_tk, bg="white")
        Rimg_mid.place(relx=1.0, rely=0.45, x=-45, y=-90, anchor='ne')  # Lateral direita, meio

        # === 3. BASE D/E (NOVAS) ===
        # rely=0.9 coloca a imagem quase no final da janela
        Limg_bot = Label(janela, image=img_tk, bg="white")
        Limg_bot.place(x=0, rely=0.9, anchor='sw')  # Lateral esquerda, base
        Rimg_bot = Label(janela, image=img_tk, bg="white")
        Rimg_bot.place(relx=1.0, rely=0.9, x=-45, anchor='se')  # Lateral direita, base
        # Nota: Ajustei o anchor para 'sw' e 'se' na base para garantir que o 'rely=0.9' 
        # seja o fundo da imagem, evitando que ela saia da tela.

    # TÍTULO
    Label(
        janela,
        text="BEM-VINDO AO COFRE DE DOCES",
        font=("Jokerman", 35, "bold"),
        fg="#701581",
        bg="white"
    ).pack(pady=60)

    # BOTÕES PRINCIPAIS
    Button(janela, text="ADICIONAR", command=desenhar_tela_adicionar, font=("Segoe UI", 20, "bold"), fg="white", bg="#701581", width=20).pack(pady=20)
    Button(janela, text="LISTAR", command=desenhar_tela_listar, font=("Segoe UI", 20, "bold"), fg="white", bg="#701581", width=20).pack(pady=20)
    Button(janela, text="DESCRIPTOGRAFAR", command=desenhar_tela_descriptografar, font=("Segoe UI", 20, "bold"), fg="white", bg="#701581", width=20).pack(pady=20)


# FUNÇÃO SALVAR
def salvar():
    """Salva um novo registro no MongoDB."""
    global entry_nome, entry_tipo, entry_qtd, entry_data

    if not DB_CONNECTED:
        messagebox.showerror("Erro de DB", "Não foi possível conectar ao MongoDB.")
        return

    try:
        nome = entry_nome.get().strip()
        tipo = entry_tipo.get().strip()
        
        # Converte para int, tratando campo vazio como 0
        qtd = int(entry_qtd.get().strip() or 0) 
        
        datahora = entry_data.get().strip()

        if not nome or not tipo or not datahora:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return

        tipo_cript = fernet.encrypt(tipo.encode('utf-8'))
        
        collection.insert_one({
            "nome": nome,
            "tipodoce": tipo_cript,
            "quantidade": qtd,
            "datahora": datahora
        })
        messagebox.showinfo("Sucesso", "Registro adicionado com sucesso!")
        
        # Limpa os campos após salvar
        entry_nome.delete(0, END)
        entry_tipo.delete(0, END)
        entry_qtd.delete(0, END)
        entry_data.delete(0, END)
        
        desenhar_tela_principal() 
        
    except ValueError:
        messagebox.showerror("Erro", "Quantidade deve ser um número inteiro!")
    except Exception as erro:
        messagebox.showerror("Erro", f"Falha ao salvar no banco: {erro}")


def desenhar_tela_adicionar():
    """Desenha a tela para adicionar um novo registro."""
    limpar_janela()
    
    global entry_nome, entry_tipo, entry_qtd, entry_data

    Label(janela, text="Adicionar Novo Doce 🍫", font=("Segoe UI", 25, "bold"), bg="white", fg="#701581").pack(pady=20)

    fields_frame = Frame(janela, bg="white")
    fields_frame.pack(pady=10)
    
    # ==== INÍCIO DOS CAMPOS ====
    
    # Campo Nome
    Label(fields_frame, text="Nome:", font=("Segoe UI", 14), bg="white").grid(row=0, column=0, sticky="w", padx=10, pady=5)
    entry_nome = Entry(fields_frame, font=("Segoe UI", 14), width=30)
    entry_nome.grid(row=0, column=1, padx=10, pady=5)
    
    # Campo Tipo de Doce
    Label(fields_frame, text="Tipo de Doce:", font=("Segoe UI", 14), bg="white").grid(row=1, column=0, sticky="w", padx=10, pady=5)
    entry_tipo = Entry(fields_frame, font=("Segoe UI", 14), width=30)
    entry_tipo.grid(row=1, column=1, padx=10, pady=5)
    
    # Campo Quantidade
    Label(fields_frame, text="Quantidade:", font=("Segoe UI", 14), bg="white").grid(row=2, column=0, sticky="w", padx=10, pady=5)
    entry_qtd = Entry(fields_frame, font=("Segoe UI", 14), width=30)
    entry_qtd.grid(row=2, column=1, padx=10, pady=5)
    
    # Campo Data/Hora
    Label(fields_frame, text="Data/Hora:", font=("Segoe UI", 14), bg="white").grid(row=3, column=0, sticky="w", padx=10, pady=5)
    entry_data = Entry(fields_frame, font=("Segoe UI", 14), width=30)
    entry_data.grid(row=3, column=1, padx=10, pady=5)

    # ==== FIM DOS CAMPOS ====

    Button(janela, text="Salvar", font=("Segoe UI", 16, "bold"), bg="#701581", fg="white", command=salvar, width=20).pack(pady=20)
    Button(janela, text="Voltar", font=("Segoe UI", 14), bg="gray90", command=desenhar_tela_principal, width=20).pack()


def listar_e_mostrar_com_filtro():
    """Busca no banco e preenche a Treeview com base no filtro.
       Toda a lógica está aqui para simplificar a rastreabilidade."""
    global list_tree, entry_list_tipo

    if not DB_CONNECTED:
        messagebox.showerror("Erro de DB", "Não foi possível conectar ao MongoDB.")
        return

    # 1. Limpa a Tabela
    for item in list_tree.get_children():
        list_tree.delete(item)

    tipo_filtro = entry_list_tipo.get().strip().lower()
    encontrado = False
    
    # 2. Busca e Popula
    try:
        for registro in collection.find():
            doce = "[ERRO DE DESCRIPTOGRAFIA]"
            try:
                # Descriptografa para poder filtrar
                doce = fernet.decrypt(registro["tipodoce"]).decode('utf-8')
            except Exception:
                pass # Em caso de erro, 'doce' permanece como a mensagem de erro

            # Aplica o filtro (se o filtro está vazio OU se o doce corresponde ao filtro)
            if not tipo_filtro or doce.lower() == tipo_filtro:
                encontrado = True
                list_tree.insert("", END, values=(
                    registro.get('nome', 'N/A'), 
                    doce, 
                    registro.get('quantidade', 'N/A'), 
                    registro.get('datahora', 'N/A')
                ))
        
        if not encontrado and tipo_filtro:
             messagebox.showinfo("Busca", "Nenhum registro encontrado para esse tipo.")
        
    except Exception as erro:
         messagebox.showerror("Erro", f"Erro ao listar registros: {erro}")


def desenhar_tela_listar():
    """Desenha a tela de listagem de registros com opção de filtro."""
    limpar_janela()
    
    global entry_list_tipo, list_tree

    Label(
        janela,
        text="Listar Doces 🍬",
        font=("Segoe UI", 25, "bold"),
        bg="white",
        fg="#701581"
    ).pack(pady=20)
    
    # Frame para o campo de filtro e botão
    filter_frame = Frame(janela, bg="white")
    filter_frame.pack(pady=10)
    
    Label(
        filter_frame,
        text="Filtrar por Tipo:",
        font=("Segoe UI", 16),
        bg="white"
    ).pack(side=LEFT, padx=10)
    
    entry_list_tipo = Entry(filter_frame, font=("Segoe UI", 14), width=20)
    entry_list_tipo.pack(side=LEFT, padx=10)
    
    # Botão que chama a função de busca
    Button(
        filter_frame,
        text="Buscar",
        font=("Segoe UI", 16, "bold"),
        bg="#701581",
        fg="white",
        command=listar_e_mostrar_com_filtro
    ).pack(side=LEFT, padx=10)
    
    # =========================================================
    # ==== CONFIGURAÇÃO DO ESTILO DA TABELA (FONTE) ===========
    # =========================================================
    style = ttk.Style()
    
    # O padrão de altura é geralmente 18-20. Vamos aumentar para 30.
    style.configure(
        "Lista.Treeview", 
        font=('Segoe UI', 14), 
        rowheight=35  # <-- ADICIONADO: Define a altura da linha em pixels
    )
                      
    # Configura o estilo para o cabeçalho da tabela (Nome, Tipo, etc.)
    style.configure("Lista.Treeview.Heading", font=('Segoe UI', 16, 'bold'))

    # Configuração do Treeview (Tabela)
    list_tree = ttk.Treeview(
        janela,
        columns=("Nome", "Tipo", "Quantidade", "Data/Hora"),
        show="headings",
        height=8,
        style="Lista.Treeview"
    )

    list_tree.heading("Nome", text="Nome")
    list_tree.column("Nome", width=150, anchor="center")

    list_tree.heading("Tipo", text="Tipo de Doce")
    list_tree.column("Tipo", width=150, anchor="center")

    list_tree.heading("Quantidade", text="Quantidade")
    list_tree.column("Quantidade", width=100, anchor="center")

    list_tree.heading("Data/Hora", text="Data/Hora")
    list_tree.column("Data/Hora", width=180, anchor="center")
    
    list_tree.pack(padx=40, pady=20, fill="x", expand=False)
    
    # Preenche a lista ao abrir a tela (sem filtro inicial)
    listar_e_mostrar_com_filtro()
    
    Button(
        janela,
        text="Voltar",
        font=("Segoe UI", 12),
        bg="gray90",
        command=desenhar_tela_principal,
        width=20
    ).pack(pady=10)



def desenhar_tela_descriptografar():
    """Desenha a tela que lista *todos* os registros com o campo 'Tipo' descriptografado."""
    limpar_janela()
    
    global decrypt_tree

    Label(
        janela,
        text="Registros Descriptografados 🧁",
        font=("Segoe UI", 25, "bold"),
        bg="white",
        fg="#701581"
    ).pack(pady=20)

    # =========================================================
    # ==== CONFIGURAÇÃO DO ESTILO DA TABELA (MESMO DE LISTAR) ==
    # =========================================================
    style = ttk.Style()
    style.configure(
        "Lista.Treeview",
        font=('Segoe UI', 14),
        rowheight=35  # mesmo tamanho da tela de listar
    )
    style.configure("Lista.Treeview.Heading", font=('Segoe UI', 16 , 'bold'))

    # Configuração do Treeview (Tabela)
    decrypt_tree = ttk.Treeview(
        janela,
        columns=("Nome", "Tipo", "Quantidade", "Data/Hora"),
        show="headings",
        height=8,
        style="Lista.Treeview"  # aplica o mesmo estilo
    )

    decrypt_tree.heading("Nome", text="Nome")
    decrypt_tree.column("Nome", width=150, anchor="center")

    decrypt_tree.heading("Tipo", text="Tipo de Doce (Descriptografado)")
    decrypt_tree.column("Tipo", width=250, anchor="center")

    decrypt_tree.heading("Quantidade", text="Quantidade")
    decrypt_tree.column("Quantidade", width=100, anchor="center")

    decrypt_tree.heading("Data/Hora", text="Data/Hora")
    decrypt_tree.column("Data/Hora", width=180, anchor="center")

    decrypt_tree.pack(padx=40, pady=20, fill="x", expand=False)

    # ==== LÓGICA DE CARREGAMENTO (DIRETA) ====
    if not DB_CONNECTED:
        messagebox.showerror("Erro de DB", "Não foi possível conectar ao MongoDB.")
    else:
        try:
            # Limpa a Tabela
            for item in decrypt_tree.get_children():
                decrypt_tree.delete(item)
            
            # Busca e Popula
            for itens in collection.find():
                doce_descriptografado = "[ERRO DE DESCRIPTOGRAFIA]"
                try:
                    doce_descriptografado = fernet.decrypt(itens["tipodoce"]).decode('utf-8')
                except Exception:
                    pass
                
                decrypt_tree.insert("", END, values=(
                    itens.get('nome', 'N/A'),
                    doce_descriptografado,
                    itens.get('quantidade', 'N/A'),
                    itens.get('datahora', 'N/A')
                ))
        except Exception as erro:
            messagebox.showerror("Erro de Listagem", f"Erro ao carregar registros: {erro}")

    # Botão Voltar
    Button(
        janela,
        text="Voltar",
        font=("Segoe UI", 14),
        bg="gray90",
        command=desenhar_tela_principal,
        width=20
    ).pack(pady=10)



# ==== INÍCIO DA APLICAÇÃO ====
desenhar_tela_principal()
janela.mainloop()
🍬 Cofre de Doces 🍭

Um sistema desktop em Python para armazenar, listar e descriptografar registros de doces, utilizando:

Tkinter para a interface gráfica

MongoDB Atlas como banco de dados

Criptografia (Fernet / AES) para proteger o tipo do doce

Pillow (PIL) para imagens

Treeview (ttk) para as tabelas

O projeto simula um cofre digital de doces, permitindo adicionar itens protegidos por criptografia e visualizar somente quando necessário.


📸 Interface

A aplicação roda em tela maximizada, com:

Imagens decorativas nas laterais

Botões grandes e estilizados

Tabelas com linhas maiores para visualização confortável

Três telas:
✔ Adicionar
✔ Listar (com filtro)
✔ Listar Descriptografado


🚀 Funcionalidades
✅ 1. Adicionar Registro

Nome do doce

Tipo do doce (criptografado antes de salvar)

Quantidade

Data/Hora

Tudo é enviado ao MongoDB

O campo Tipo de Doce é criptografado usando Fernet:

tipo_cript = fernet.encrypt(tipo.encode('utf-8'))

✅ 2. Listar Doces (com Filtro)

Tabela estilizada com:

Nome

Tipo (descriptografado apenas para filtrar)

Quantidade

Data/Hora

Campo para filtrar pelo tipo do doce

Busca em tempo real

Se o tipo inserido não existir, aparece um aviso.

✅ 3. Descriptografar Todos os Doces

Uma tela que mostra todos os registros com o tipo de doce já descriptografado, ideal para auditoria.

Se o dado tiver sido criptografado incorretamente, o sistema mostra:

[ERRO DE DESCRIPTOGRAFIA]


🔐 Criptografia

O projeto utiliza Fernet (da biblioteca cryptography), que implementa criptografia AES + HMAC, garantindo:

Confidencialidade

Integridade

Autenticação

A mesma chave é usada para criptografar e descriptografar:

key = b'AD5BIGDLa34gtAtmKkVSI_c4pHGPOizinaA5Ya-k2Mw='
fernet = Fernet(key)


🗄️ Banco de Dados (MongoDB)

A aplicação conecta-se ao MongoDB Atlas (na nuvem):

doces = MongoClient("mongodb+srv://123:123@meubanco.apcmzzs.mongodb.net/")
collection = doces["CofredeDoces"]["Registros"]


Cada registro tem o formato:

{
  "nome": "Chocolate",
  "tipodoce": "<criptografado>",
  "quantidade": 5,
  "datahora": "10/11/2025 15:00"
}


🎨 Interface (Tkinter)

O projeto usa:

pack, grid e place combinados

Uso de Label, Entry, Button, Treeview

Função limpar_janela() para trocar telas dinamicamente

Imagens decorativas com PIL.ImageTk

A UI foi montada para ser simples e limpa.


📂 Estrutura de Telas
🏠 Tela Principal

Botão ADICIONAR

Botão LISTAR

Botão DESCRIPTOGRAFAR

Imagens laterais

➕ Tela de Adicionar

Quatro campos (nome, tipo, quantidade, data/hora)

Botão Salvar

Botão Voltar

📋 Tela de Listagem

Campo de filtro por tipo

Botão Buscar

Tabela com dados descriptografados parcialmente

Botão Voltar

🔓 Tela de Descriptografar

Lista todos os registros já descriptografados

Tabela com quatro colunas

Botão Voltar


▶ Como Executar o Projeto
1. Instale os requisitos:
pip install pymongo cryptography pillow


(Tkinter já vem com Python em Windows e Linux)

2. Execute o programa:
python app.py


🧱 Tecnologias Utilizadas
Tecnologia	Uso
Python 3	Linguagem principal
Tkinter	Interface gráfica
MongoDB Atlas	Banco de dados na nuvem
cryptography (Fernet)	Criptografia AES
Pillow (PIL)	Manipulação de imagens
ttk.Treeview	Exibição de tabelas


📌 Observações Importantes

A chave Fernet deve ser mantida em segredo

O caminho da imagem deve existir no PC do usuário

O sistema já trata erros de conexão e descriptografia

Caso o banco caia, o app continua funcionando com mensagens de erro amigáveis

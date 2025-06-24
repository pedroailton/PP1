import os            # Biblioteca para comandos do sistema operacional (como limpar a tela)
import sqlite3       # Biblioteca padrão do Python para usar banco de dados SQLite
import msvcrt        # Biblioteca do Windows para captura de teclas (funciona apenas no Windows)

# ===== UTILITÁRIOS =====

def limpar_tela():
    # Limpa a tela do terminal no Windows
    os.system('cls')

def nome_valido(nome):
    # Verifica se o nome contém apenas caracteres válidos
    if not nome:
        return False
    for c in nome:
        if not ((c.isalnum()) or (c.isspace()) or (c in "'.,!?\"-")):
            return False
    return True

def nome_ja_existe(nome):
    #Verifica se o nome já foi adicionado no banco de dados
    cursor.execute("SELECT COUNT(*) FROM cartoes WHERE nome = ?", (nome,))
    return cursor.fetchone()[0] > 0

def ler_tecla():
    # Lê uma tecla pressionada pelo usuário (sem precisar apertar ENTER)
    tecla = msvcrt.getch()
    if tecla:
        return tecla.decode('utf-8')
    else:
        return ''

# ===== BANCO DE DADOS =====

# Conexão com o banco SQLite (será criado um arquivo "cardume.db" se não existir)
conn = sqlite3.connect('cardume.db')
cursor = conn.cursor()  # Cursor usado para executar comandos SQL

def inicializar_banco():
    # Cria a tabela "cartoes" no banco se ainda não existir
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cartoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            coluna TEXT NOT NULL
        )
    ''')
    conn.commit()  # Confirma as mudanças no banco
    carregar_tarefas_do_banco()  # Carrega os dados da tabela para o programa

# Estrutura de dados em memória para manter os cartões organizados por coluna
tarefas = {
    "A Fazer": [],
    "Executando": [],
    "Pronto": []
}

def carregar_tarefas_do_banco():
    # Limpa as colunas atuais
    for coluna in tarefas:
        tarefas[coluna] = []

    # Busca todos os cartões do banco
    cursor.execute('SELECT id, nome, coluna FROM cartoes')
    for id_, nome, coluna in cursor.fetchall():
        if coluna in tarefas:
            tarefas[coluna].append({'id': id_, 'nome': nome})

def salvar_cartao_banco(nome, coluna):
    # Insere novo cartão no banco
    cursor.execute('INSERT INTO cartoes (nome, coluna) VALUES (?, ?)', (nome, coluna))
    conn.commit()
    carregar_tarefas_do_banco()  # Atualiza os dados em memória

def atualizar_nome_cartao(id_, novo_nome):
    # Atualiza o nome de um cartão no banco
    cursor.execute('UPDATE cartoes SET nome = ? WHERE id = ?', (novo_nome, id_))
    conn.commit()
    carregar_tarefas_do_banco()

def mover_cartao(id_, nova_coluna):
    # Atualiza a coluna (posição) de um cartão no banco
    cursor.execute('UPDATE cartoes SET coluna = ? WHERE id = ?', (nova_coluna, id_))
    conn.commit()
    carregar_tarefas_do_banco()

def remover_cartao(id_):
    # Remove um cartão do banco de dados
    cursor.execute('DELETE FROM cartoes WHERE id = ?', (id_,))
    conn.commit()
    carregar_tarefas_do_banco()

# ===== FUNÇÕES DO SISTEMA KANBAN =====

def exibir_tarefas():
    # Mostra os cartões na tela separados por coluna
    print("\n======== TAREFAS ========")
    for coluna in ["A Fazer", "Executando", "Pronto"]:
        print(f"\n[{coluna}]")
        for cartao in tarefas[coluna]:
            print(f"ID: {cartao['id']} | Nome: {cartao['nome']}")
    print("=========================\n")

def encontrar_cartao_por_id(id_busca):
    # Procura um cartão pelo ID e retorna o cartão e a coluna onde ele está
    for coluna in tarefas:
        for cartao in tarefas[coluna]:
            if str(cartao["id"]) == id_busca:
                return cartao, coluna
    return None, None

def adicionar_cartao():
    while True:
        limpar_tela()
        print("[ADICIONAR CARTÃO] Pressione ESC a qualquer momento para voltar.")
        print("Digite o nome do cartão (máx. 80 caracteres):")

        nome = "" #configura a variável nome como string
        while True: #Laço infinito para capturar todas as teclas até o usuário apertar ESC ou ENTER
            char = ler_tecla()
            if not char:
                continue
            if ord(char) == 27: #Checa se o código numérico do caractere é 27, que é o valor ASCII da tecla ESC.
                return
            elif char in ('\r', '\n'): #Verifica se o caractere é ENTER, que pode ser representado como '\r' (carriage return) ou '\n' (newline).
                break
            elif char == '\x08': #Verifica se a tecla pressionada foi Backspace. '\x08' é o caractere de retrocesso.
                nome = nome[:-1] #Apaga o último caractere
                print('\b \b', end='', flush=True) # Remove visualmente o caractere do terminal
            else: #Se o caractere digitado não for ESC, ENTER nem BACKSPACE, ele é um caractere comum.
                nome += char
                print(char, end='', flush=True)

        nome = nome.strip() #Tira os espaços na string nome

        if not nome:
            print("\n❌ O nome não pode estar vazio.")
            input("Pressione ENTER para tentar novamente.")
            continue

        if len(nome) > 80:
            print("\n❌ Nome muito longo.")
            input("Pressione ENTER para tentar novamente.")
            continue

        if not nome_valido(nome):
            print("\n❌ Nome inválido. Use apenas letras, números, espaços e pontuação simples ('.,!?\"-').")
            input("Pressione ENTER para tentar novamente.")
            continue

        if nome_ja_existe(nome):
            print("\n⚠️ Um cartão com esse nome já existe.")
            print("Pressione ENTER para continuar assim mesmo ou ESC para cancelar.")
            tecla = ler_tecla()
            if not char:
                continue
            if not ord(tecla) == 13: # Só salva o cartão se a tecla pressionada for Enter
                continue

        salvar_cartao_banco(nome, "A Fazer") # Salva automaticamente o nome adicionado na coluna "A fazer"
        print("\n✅ Cartão adicionado com sucesso!")
        print("Pressione ESC para voltar ou ENTER para adicionar outro.")
        tecla = ler_tecla()
        if not char:
            continue
        if ord(tecla) == 27:
            return

def editar_cartao():
    while True:
        limpar_tela()
        exibir_tarefas()
        print("[EDITAR CARTÃO] Digite o ID do cartão que deseja editar (ESC para voltar):")
        entrada = ""
        while True:
            char = ler_tecla()
            if not char:
                continue
            if ord(char) == 27:
                return
            elif char in ('\r', '\n'):
                break
            else:
                entrada += char
                print(char, end='', flush=True)

        cartao, coluna = encontrar_cartao_por_id(entrada.strip())
        if not cartao:
            print("\n❌ ID inválido.")
            input("Pressione ENTER para continuar.")
            continue

        limpar_tela()
        print("1 - Mudar nome do cartão")
        print("2 - Mudar posição do cartão")
        acao = input("Escolha uma opção (1 ou 2): ").strip()

        if acao == "1":
            print("Digite o novo nome (ESC para cancelar):")
            novo_nome = ""
            while True:
                char = ler_tecla()
                if not char:
                    continue
                if ord(char) == 27:
                    return
                elif char in ('\r', '\n'):
                    break
                elif char == '\x08':
                    novo_nome = novo_nome[:-1]
                    print('\b \b', end='', flush=True)
                else:
                    novo_nome += char
                    print(char, end='', flush=True)

            novo_nome = novo_nome.strip()
            if len(novo_nome) > 80 or not nome_valido(novo_nome):
                print("\n❌ Nome inválido.")
                input("Pressione ENTER para continuar.")
                continue

            atualizar_nome_cartao(cartao["id"], novo_nome)
            print("\n✅ Nome atualizado.")
            input("Pressione ENTER para continuar.")

        elif acao == "2":
            print("Mover para:")
            print("1 - A Fazer")
            print("2 - Executando")
            print("3 - Pronto")
            destino = input("Escolha: ").strip()
            nova_coluna = {"1": "A Fazer", "2": "Executando", "3": "Pronto"}.get(destino)

            if nova_coluna:
                if nova_coluna == "Executando" and len(tarefas["Executando"]) >= 10:
                    print("⚠️ Já há 10 tarefas em 'Executando'.")
                else:
                    mover_cartao(cartao["id"], nova_coluna)
                    print(f"✅ Cartão movido para '{nova_coluna}'.")
            else:
                print("❌ Opção inválida.")
            input("Pressione ENTER para continuar.")
        else:
            print("❌ Opção inválida.")
            input("Pressione ENTER para continuar.")

def excluir_cartao():
    while True:
        limpar_tela()
        exibir_tarefas()
        print("[EXCLUIR CARTÃO] Digite o ID do cartão que deseja excluir (ESC para voltar):")
        entrada = ""
        while True:
            char = ler_tecla()
            if not char:
                continue
            if ord(char) == 27:
                return
            elif char in ('\r', '\n'):
                break
            else:
                entrada += char
                print(char, end='', flush=True)

        cartao, coluna = encontrar_cartao_por_id(entrada.strip())
        if not cartao:
            print("\n❌ ID inválido.")
            input("Pressione ENTER para continuar.")
            continue

        print("\nPressione ENTER para confirmar exclusão ou ESC para cancelar.")
        tecla = ler_tecla()
        if not char:
            continue
        if ord(char) == 27:
            return


        remover_cartao(cartao["id"])
        print("✅ Cartão excluído com sucesso.")
        input("Pressione ENTER para continuar.")

def menu_cardume():
    # Menu principal do programa
    while True:
        limpar_tela()
        print(".><_>" * 6)
        print(" " * 8 + "CARDUME")
        print("<_><." * 6)
        exibir_tarefas()

        print("1 - Adicionar cartão")
        print("2 - Editar cartão")
        print("3 - Excluir cartão")
        print("4 - Fechar programa")

        escolha = input("Digite sua escolha: ").strip()

        if escolha == "1":
            adicionar_cartao()
        elif escolha == "2":
            editar_cartao()
        elif escolha == "3":
            excluir_cartao()
        elif escolha == "4":
            print("Encerrando...")
            break
        else:
            print("Opção inválida.")
            input("Pressione ENTER para continuar.")

# ===== INICIALIZAÇÃO =====
if __name__ == "__main__":
    inicializar_banco()  # Cria a tabela e carrega dados
    menu_cardume()       # Inicia o menu principal
    conn.close()         # Fecha a conexão com o banco ao programa ser fechado
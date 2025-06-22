
import os
import uuid
import msvcrt

# ===== UTILITÁRIOS =====

def limpar_tela():
    os.system('cls')

def gerar_id():
    return str(uuid.uuid4())[:8]

def nome_valido(nome):
    for c in nome:
        if not (c.isalnum() or c.isspace() or c in "'.,!?\"-"):
            return False
    return True

def ler_tecla():
    tecla = msvcrt.getch()
    return tecla.decode('utf-8') if tecla else ''

# ===== DADOS =====

tarefas = {
    "A Fazer": [],
    "Executando": [],
    "Pronto": []
}

# ===== FUNÇÕES =====

def exibir_tarefas():
    print("\n======== TAREFAS ========")
    for coluna in ["A Fazer", "Executando", "Pronto"]:
        print(f"\n[{coluna}]")
        for cartao in tarefas[coluna]:
            print(f"ID: {cartao['id']} | Nome: {cartao['nome']}")
    print("=========================\n")

def encontrar_cartao_por_id(id_busca):
    for coluna in tarefas:
        for cartao in tarefas[coluna]:
            if cartao["id"] == id_busca:
                return cartao, coluna
    return None, None

def adicionar_cartao():
    while True:
        limpar_tela()
        print("[ADICIONAR CARTÃO] Pressione ESC a qualquer momento para voltar.")
        print("Digite o nome do cartão (máx. 80 caracteres):")

        nome = ""
        while True:
            char = ler_tecla()
            if ord(char) == 27:  # ESC
                return
            elif char in ('\r', '\n'):
                break
            elif char == '\x08':  # Backspace
                nome = nome[:-1]
                print('\b \b', end='', flush=True)
            else:
                nome += char
                print(char, end='', flush=True)

        nome = nome.strip()
        if len(nome) > 80:
            print("\n❌ Nome muito longo.")
            input("Pressione ENTER para tentar novamente.")
            continue

        if not nome_valido(nome):
            print("\n❌ Nome inválido. Use apenas letras, números, espaços e pontuação simples.")
            input("Pressione ENTER para tentar novamente.")
            continue

        novo_cartao = {"id": gerar_id(), "nome": nome}
        tarefas["A Fazer"].append(novo_cartao)
        print("\n✅ Cartão adicionado com sucesso!")
        print("Pressione ESC para voltar ou ENTER para adicionar outro.")
        tecla = ler_tecla()
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

            if len(novo_nome) > 80 or not nome_valido(novo_nome):
                print("\n❌ Nome inválido.")
                input("Pressione ENTER para continuar.")
                continue
            cartao["nome"] = novo_nome
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
                    tarefas[coluna].remove(cartao)
                    tarefas[nova_coluna].append(cartao)
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
        if ord(tecla) == 27:
            return

        tarefas[coluna].remove(cartao)
        print("✅ Cartão excluído com sucesso.")
        input("Pressione ENTER para continuar.")

def menu_cardume():
    while True:
        limpar_tela()
        print("=" * 40)
        print(" " * 10 + "CARDUME")
        print("=" * 40)
        exibir_tarefas()

        print("1 - Adicionar cartão")
        print("2 - Editar cartão")
        print("3 - Excluir cartão")
        print("4 - Fechar programa")

        escolha = input("Digite sua escolha (1-4): ").strip()

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
            print("❌ Opção inválida.")
            input("Pressione ENTER para continuar.")

# ===== INICIAR =====
menu_cardume()

import tkinter

if __name__ == '__main__':

    def estimar_livros_futuros(digitais, fisicos):
        # Função para estimar livros nos próximos 5 anos
        total = digitais + fisicos
        futuro = total * 5
        if futuro >= 100:
            print(f"\nIncrível!\nSe continuar nesse ritmo, você pode ler cerca de {futuro} livros nos próximos 5 anos!")
        elif 40 <= futuro < 100:
            print(f"\nMuito bom!\nVocê poderá ler aproximadamente {futuro} livros em 5 anos.")
        else:
            print(f"\nVamos aumentar a leitura? Ela é um hábito importante.\nVocê pode ler cerca de {futuro} livros nos próximos 5 anos.")

    def calcular_horas_anuais(horas_semanais):
        # Função para calcular o tempo anual com base em horas semanais
        return horas_semanais * 52
    
    def estimar_paginas_por_ano(livros):
        # Função adicional: estimar páginas lidas por ano
        media_paginas = 300
        return livros * media_paginas

    def impacto_na_vida(idade, horas_estudo_ano):
        # Função adicional: estimar impacto de leitura na vida acadêmica
        if idade < 18 and horas_estudo_ano > 300:
            return "Você está em ótima fase de aprendizado, continue assim!"
        elif idade >= 18 and horas_estudo_ano > 500:
            return "Seu comprometimento com o conhecimento é exemplar!"
        else:
            return "Considere aumentar suas horas de estudo para melhor desempenho."

    # Coleta de dados do usuário
    print("🔍 Bem-vindo ao Relatório do Leitor!\n")

    nome = input("Digite seu primeiro nome: ")

    idade = int(input("Digite sua idade: "))

    cidade = input("Cidade: ")

    estado = input("Estado: ")

    livros_digitais = int(input("Quantos livros digitais você leu no último ano? "))

    livros_fisicos = int(input("Quantos livros físicos você leu no último ano? "))

    preferencia = input("Você prefere ler em formato Digital ou Físico? ")

    horas_estudo_semana = float(input("Quantas horas por semana você estuda com livros? "))

    horas_entretenimento_semana = float(input("Quantas horas por semana você lê por entretenimento? "))

    profissao = input("Qual sua ocupação ou área de interesse? ")

    # Mensagem de boas-vindas e contexto
    print(f"\n🎉 Olá, {nome}! Que bom ter alguém de {cidade}, {estado} aqui.")
    if idade < 18:
        print("Você está em uma fase excelente para desenvolver bons hábitos de leitura desde cedo!\nIsso pode mudar sua vida e seu futuro.")
    elif idade <= 30:
        print("A leitura pode ser um diferencial enorme em sua vida profissional e pessoal.\nAproveite!")
    else:
        print("Nunca é tarde para aprender e explorar novos mundos através da leitura!\nContinue buscando!")

    # Estimativas
    estimar_livros_futuros(livros_digitais, livros_fisicos)

    horas_estudo_ano = calcular_horas_anuais(horas_estudo_semana)
    horas_entretenimento_ano = calcular_horas_anuais(horas_entretenimento_semana)

    print(f"\n📘 Você estuda aproximadamente {horas_estudo_ano:.1f} horas por ano com livros.")
    print(f"📖 E lê cerca de {horas_entretenimento_ano:.1f} horas por ano por lazer.")

    # Funções criativas
    total_livros = livros_digitais + livros_fisicos
    total_paginas = estimar_paginas_por_ano(total_livros)
    print(f"📄 Estimamos que você leu cerca de {total_paginas} páginas no último ano (média de 250 páginas por livro).")

    impacto = impacto_na_vida(idade, horas_estudo_ano)
    print(f"\n💡 {impacto}")

    # Preferência
    print(f"\nSua preferência por leitura é: {preferencia}. Isso nos ajuda a entender suas preferências e indicar boas práticas!")

    # Ocupação
    print(f"Área de interesse: {profissao}. Leitura é uma ferramenta poderosa em qualquer profissão!")

    print("\n✨ Obrigado por utilizar nosso programa! Continue cultivando o hábito da leitura!")

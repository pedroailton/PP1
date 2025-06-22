hoje = 'terça'
quantidade_de_lixeiros = 3
porta_fechada = True
porta_trancada = True
sacolas_na_gaveta = 15

if (hoje == 'terça') or (hoje == 'quinta') or (hoje == 'sábado'):  # O caminhão do lixo só passa nesses dias na minha rua
    vá_na_cozinha_até_a_gaveta_de_sacolas_de_compras()

    if sacolas_na_gaveta >= 3:
        pegue_3_sacolas()
    else:
        pegue_quantas_sacolas_houver()
        procure_mais_sacolas_para_completar_3()

    ponha_3_sacolas_na_mesa_da_cozinha()

    for indice in range(0, quantidade_de_lixeiros):
        pegue_uma_sacola()
        vá_ao_banheiro(indice)
        abra_o_lixeiro()
        recolha_o_saco_de_lixo()
        coloque_novo_saco_no_lixeiro()
        feche_o_lixeiro()

    amarre_os_sacos_de_lixo_juntos()

    if porta_fechada and porta_trancada:
        procure_chave_para_abrir_porta()
        abra_a_porta_com_a_chave()
        abre_a_porta()
    elif porta_fechada and not porta_trancada:
        abre_a_porta()

    ande_até_o_poste_perto_de_casa()
    coloque_o_lixo_no_local()

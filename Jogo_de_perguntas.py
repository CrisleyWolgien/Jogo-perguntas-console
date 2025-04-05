import json
import random
import time
import sys


def recarregar_json():
    with open("perguntas.json", encoding="utf-8") as file:
        perguntas = json.load(file)  # abre o json
    return perguntas


with open("perguntas.json", encoding="utf-8") as file:
    perguntas = json.load(file)  # abre o json


id_perguntas = {int(k): v for k, v in perguntas.items()}# tranforma o id em in
perguntas_tamanho_dict = len(perguntas)  # define o tamanho de dicionario
print(id_perguntas.keys())  # imprime os ids das perguntas
id_perguntas_lista = list(id_perguntas.keys())  # transforma o id em lista


# inicializacao de dados
respostas_corretas = 0
respostas_erradas = 0
rodadas_jogadas = 0


def randomiza_pergunta():
    random_da_pergunta = random.choice(id_perguntas_lista)  # define o range do random conforme o tamanho do dicionário
    return random_da_pergunta


perguntas_ja_respondidas = []


def pergunta(
    pergunta_selecionada,
):  # cria uma funcao para ser chamado no futuro junto com os print para o console
    nome = ""  # Nome da pergunta
    opcoes = ["", "", "", ""]

    for pergunta_selecionada_k, pergunta_selecionada_v in pergunta_selecionada.items():
        if pergunta_selecionada_k == "pergunta":
            nome = pergunta_selecionada_v
        elif pergunta_selecionada_k == "opcoes":
            opcoes = list(pergunta_selecionada_v)
            opcoes += [""] * (4 - len(opcoes))
        else:
            resposta = pergunta_selecionada_v
    return nome, *opcoes[:4], resposta


def jogar(respostas_corretas, respostas_erradas):
    random_pergunta_selecionada = randomiza_pergunta()

    while random_pergunta_selecionada in perguntas_ja_respondidas:
        random_pergunta_selecionada = randomiza_pergunta()
    perguntas_ja_respondidas.append(random_pergunta_selecionada)

    pergunta_selecionada = id_perguntas[random_pergunta_selecionada]
    nome_pergunta, opcao_1, opcao_2, opcao_3, opcao_4, resposta_pergunta = pergunta(pergunta_selecionada)

    # corpo da pergunta
    print()
    print(nome_pergunta)
    print()
    print(opcao_1)
    print(opcao_2)
    print(opcao_3)
    print(opcao_4)
    print()
    print("Responda a alternativa correta")
    resposta_do_user = input()
    while resposta_do_user != "1" and resposta_do_user != "2" and resposta_do_user != "3" and resposta_do_user != "4":
        print("responda uma alternativa valida")
        resposta_do_user = input()
        resposta_do_user = resposta_do_user

    if int(resposta_do_user) == int(resposta_pergunta):
        print("parabens você acertou")
        respostas_corretas += 1

    else:
        print("que pena você errou")
        respostas_erradas += 1
    return respostas_corretas, respostas_erradas


# adiciona pergunta


def adiciona_pergunta():
    id_nova_pergunda = max(id_perguntas.keys()) + 1
    novo_nome_pergunta = input("Digite o nome da pergunta: ")
    opcao = []
    opcao_i = 1
    while opcao_i < 5:
        nova_opcao = input(f"Digite a opção {opcao_i}: ")
        opcao.append(str(opcao_i) + "." + nova_opcao)
        opcao_i += 1
    nova_resposta = input("Insira a Resposta (Em numero de 1 a 4):  ")
    while int(nova_resposta) not in [1, 2, 3, 4]:
        print("Valor invalido")
        nova_resposta = input("Insira a Resposta (Em numero de 1 a 4):  ")

    perguntas[str(id_nova_pergunda)] = {
        "pergunta": novo_nome_pergunta,
        "opcoes": opcao,
        "resposta": int(nova_resposta),
    }

    with open("perguntas.json", "w", encoding="utf-8") as file:
        json.dump(perguntas, file, indent=4, ensure_ascii=False)
    recarregar_json()
    print("pergunta adicionada com sucesso")
    time.sleep(1)


# EXCLUIR PERGUNTA
def excluir_pergunta():
    print("Escolha o id da pergunta que deseja excluir")
    print("id das perguntas disponíveis")
    for pergunta_id in perguntas.keys():
        pergunta_selecionada = id_perguntas[int(pergunta_id)]
        nome_pergunta, opcao_1, opcao_2, opcao_3, opcao_4, resposta_pergunta = pergunta(pergunta_selecionada)
        print()
        print(pergunta_id + " - " + nome_pergunta)
    pergunta_selecionada_excluir = input(f"Digite o id da pergunta que deseja excluir: ")
    while pergunta_selecionada_excluir not in perguntas.keys():
        print("pergunta não encontrada")
        pergunta_selecionada_excluir = input(f"Digite o id da pergunta que deseja excluir: ")
    del perguntas[pergunta_selecionada_excluir]
    with open("perguntas.json", "w", encoding="utf-8") as file:
        json.dump(perguntas, file, indent=4, ensure_ascii=False)
    recarregar_json()
    print("pergunta excluida com sucesso")
    time.sleep(1)


# menu do programa
sair_progrma = False


def menu(rodadas_jogadas, respostas_corretas, respostas_erradas, sair_progrma):
    recarregar_json()
    print()
    print("Bem vindo ao Jogo de perguntas")
    print("Escolha uma opção")
    print()
    print("1.Jogar")
    print("2.Adicionar pergunta")
    print("3.Excluir pergunta")
    print("0.Sair")
    print()
    resposta_do_user = input("responda uma alternativa valida: ")
    while resposta_do_user not in ["0", "1", "2", "3", "4"]:
        resposta_do_user = input("responda uma alternativa valida: ")

    resposta_do_user = int(resposta_do_user)

    match resposta_do_user:
        case 1:
            print("Você selecionou Jogar")
            print("quantas rodadas vai querer")
            print(f"de 1 a {perguntas_tamanho_dict}")
            rodadas_selecionada = input()
            while int(rodadas_selecionada) > perguntas_tamanho_dict:
                print("você escolheu um numero incompatível")
                print(f"escolha um numero de 1 a {perguntas_tamanho_dict}")
                rodadas_selecionada = input()
            while rodadas_jogadas < int(rodadas_selecionada):
                print(f"\nRodada {rodadas_jogadas + 1}")
                respostas_corretas, respostas_erradas = jogar(respostas_corretas, respostas_erradas)
                rodadas_jogadas += 1
            print("voce finalizou o jogo ")
            print()
            print("--------Placar--------")
            print(f"Você jogou um total de {rodadas_jogadas} rodadas")
            print(f"Você acertou um total de {respostas_corretas} respostas")
            print(f"Você errou um total de {respostas_erradas} respostas")
            time.sleep(1)
            print()

        case 2:
            adiciona_pergunta()
        case 3:
            excluir_pergunta()
        case 0:
            print("vc saiu")
            sys.exit()

while not sair_progrma:
    menu(rodadas_jogadas, respostas_corretas, respostas_erradas, sair_progrma)

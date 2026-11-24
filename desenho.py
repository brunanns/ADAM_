from fases import progresso_do_marco
import math

import estado
from config import W, H, PHASES, ENEMY_TYPES
from efeitos import quadro_da_explosao
from utils import texto, texto_centralizado, desenhar_imagem_mundo, desenhar_imagem_tela, desenhar_barras

state = estado.state


def desenhar_jogo():
    desenhar_chao()
    desenhar_tom_da_fase()
    desenhar_obstaculos()
    desenhar_itens()
    desenhar_historia()
    desenhar_inimigos()
    desenhar_tiros()
    desenhar_filha()
    desenhar_jogador()
    desenhar_efeitos()
    desenhar_flash_dano()
    desenhar_hud()
    desenhar_dialogo()


def desenhar_chao():
    camera = state["camera"]
    primeira_coluna = int(camera[0] // 80)
    primeira_linha = int(camera[1] // 80)

    for linha in range(primeira_linha, primeira_linha + 8):
        for coluna in range(primeira_coluna, primeira_coluna + 11):
            indice = state["chao"][linha][coluna]
            desenhar_imagem_tela("tile_%02d" % indice, coluna * 80 - camera[0], linha * 80 - camera[1])


def desenhar_tom_da_fase():
    if state["fase"] == 1:
        desenhar_imagem_tela("tom_fase2", 0, 0)
    elif state["fase"] >= 2:
        desenhar_imagem_tela("tom_fase3", 0, 0)


def desenhar_sombra(x, y, nome_da_imagem):
    imagem = estado.imagens[nome_da_imagem]
    nome = "sombra_g" if imagem.width > 60 else "sombra"
    desenhar_imagem_mundo(nome, x, y + imagem.height / 2 - 6)


def desenhar_efeitos():
    for efeito in state["efeitos"]:
        if efeito["tempo"] >= 0:
            desenhar_imagem_mundo("explosao_" + str(quadro_da_explosao(efeito)), efeito["x"], efeito["y"])


def desenhar_flash_dano():
    # a tela fica vermelha nas bordas logo depois de levar dano
    if state["jogador"]["invencivel"] > 0.2:
        desenhar_imagem_tela("flash_dano", 0, 0)


def desenhar_obstaculos():
    camera = state["camera"]
    for bloco in state["obstaculos"]:
        visivel = (
            bloco["x"] + bloco["w"] > camera[0]
            and bloco["x"] < camera[0] + W
            and bloco["y"] + bloco["h"] > camera[1]
            and bloco["y"] < camera[1] + H
        )
        if visivel:
            imagem = "porta" if "porta" in bloco else "bloco"
            for i in range(bloco["nx"]):
                for j in range(bloco["ny"]):
                    desenhar_imagem_mundo(imagem, bloco["x"] + i * 40 + 20, bloco["y"] + j * 40 + 20)


def desenhar_itens():
    for item in state["itens"]:
        desenhar_imagem_mundo(item["tipo"], item["x"], item["y"])


def desenhar_inimigos():
    camera = state["camera"]
    for inimigo in state["inimigos"]:
        dados = ENEMY_TYPES[inimigo["tipo"]]
        quadros = dados.get("frames")
        if quadros:
            indice = min(inimigo.get("anim_frame", 0), len(quadros) - 1)
            imagem = quadros[indice]
        else:
            imagem = dados["img"]
        desenhar_sombra(inimigo["x"], inimigo["y"], imagem)
        desenhar_imagem_mundo(imagem, inimigo["x"], inimigo["y"])

        # barrinha de vida em cima do inimigo
        quantidade = 10
        cheia = math.ceil(quantidade * inimigo["hp"] / inimigo["vida_max"])
        x = inimigo["x"] - quantidade * 2 - camera[0]
        y = inimigo["y"] - inimigo["raio"] - 10 - camera[1]
        for i in range(quantidade):
            if i < cheia:
                desenhar_imagem_tela("segc", x + i * 4, y)
            else:
                desenhar_imagem_tela("segv", x + i * 4, y)


def desenhar_tiros():
    for tiro in state["tiros"]:
        desenhar_imagem_mundo("tiro", tiro["x"], tiro["y"])
    for tiro in state["tiros_inimigos"]:
        desenhar_imagem_mundo("tiro_in", tiro["x"], tiro["y"])


def desenhar_jogador():
    jogador = state["jogador"]
    direcao = jogador["direcao"]
    desenhar_sombra(jogador["x"], jogador["y"], "adam_" + str(direcao))

    if jogador["andando"]:
        nome = "adam_andando_%d_%d" % (direcao, jogador["anim_frame"])
    else:
        nome = "adam_" + str(direcao)
    piscando = jogador["invencivel"] > 0 and int(jogador["invencivel"] * 20) % 2
    if not piscando:
        desenhar_imagem_mundo(nome, jogador["x"], jogador["y"])


def desenhar_filha():
    filha = state["filha"]
    if filha:
        desenhar_imagem_mundo("filha", filha["x"], filha["y"])


def desenhar_historia():
    for pista in state["pistas"]:
        if pista["lida"]:
            desenhar_imagem_mundo("pista_lida", pista["x"], pista["y"])
        else:
            desenhar_imagem_mundo("pista", pista["x"], pista["y"])
    for sobrevivente in state["sobreviventes"]:
        desenhar_sombra(sobrevivente["x"], sobrevivente["y"], "sobrevivente")
        desenhar_imagem_mundo("sobrevivente", sobrevivente["x"], sobrevivente["y"])
    if state["terminal"]:
        desenhar_imagem_mundo("terminal", state["terminal"]["x"], state["terminal"]["y"])

    # aviso "[E] ..." em cima do objeto que está perto do Adam
    alvo = state["interagir"]
    if alvo:
        rotulos = {"pista": "investigar", "sobrevivente": "falar", "terminal": "acessar terminal"}
        camera = state["camera"]
        texto("[E] " + rotulos[alvo["tipo"]], alvo["x"] - 45 - camera[0], alvo["y"] - 40 - camera[1], 13, (91, 197, 190))


def desenhar_dialogo():
    # caixa de diálogo pequena: o jogo continua rodando por trás
    dialogo = state["dialogo"]
    if dialogo:
        desenhar_imagem_tela("caixa_dialogo", 20, 370)
        texto(dialogo["titulo"], 40, 382, 17, (91, 197, 190))
        for i, linha in enumerate(dialogo["linhas"]):
            texto(linha, 40, 410 + i * 24, 15)


ROTULOS_MARCO = {"abates": "Robôs", "pistas": "Registros", "sobrevivente": "Sobreviventes"}


def desenhar_hud():
    jogador = state["jogador"]

    desenhar_imagem_tela("hud_panel", 8, 6)
    desenhar_imagem_tela("score_panel", W - 198, 6)
    desenhar_imagem_tela("objective_panel", 8, H - 54)

    desenhar_barras("hp", jogador["hp"], jogador["vida_max"], 12, 12)
    texto("%d/%d" % (math.ceil(jogador["hp"]), jogador["vida_max"]), 95, 12, 14)
    desenhar_barras("xp", jogador["xp"], jogador["xp_proximo"], 12, 34, arredondar_para_cima=False)
    texto("Nível %d" % jogador["nivel"], 12, 46, 16)
    texto("Pontos: %d" % state["score"], W - 160, 12, 18)

    # Barra especial do chefe: destaca o confronto e deixa a vida visível
    # sem depender apenas da pequena barra acima do sprite.
    chefe = next((i for i in state["inimigos"] if ENEMY_TYPES[i["tipo"]]["boss"]), None)
    if chefe:
        nome_chefe = ENEMY_TYPES[chefe["tipo"]]["nome"]
        texto_centralizado(nome_chefe.upper(), 27, 16, (235, 105, 75))
        desenhar_barras("hp", chefe["hp"], chefe["vida_max"], W / 2 - 180, 48, quantidade=90)

    if state["filha"]:
        texto_fase = "Encontre sua filha!"
    elif state["terminal"]:
        texto_fase = "Acesse o terminal [E]"
    elif state["boss_ativo"]:
        texto_fase = "BOSS em combate"
    else:
        progresso = progresso_do_marco()
        if progresso:
            atual, total, marco = progresso
            texto_fase = "%s: %d/%d" % (ROTULOS_MARCO[marco["tipo"]], atual, total)
        else:
            texto_fase = "Entre na sala do chefe"
    texto(texto_fase, W - 160, 36, 15, (170, 170, 170))

    lidas = 0
    for pista in state["pistas"]:
        if pista["lida"]:
            lidas += 1
    texto("Pistas: %d/%d" % (lidas, len(state["pistas"])), W - 160, 53, 12, (91, 197, 190))

    progresso = progresso_do_marco()
    if progresso and not (state["boss_ativo"] or state["terminal"] or state["filha"]):
        objetivo = progresso[2]["texto"]
    else:
        objetivo = PHASES[state["fase"]]["objetivo"]
    texto("Objetivo: " + objetivo, 12, H - 46, 14, (217, 130, 43))

    if state["melhorias"]:
        melhorias = ", ".join(state["melhorias"])
    else:
        melhorias = "nenhuma"
    texto("Melhorias: " + melhorias, 12, H - 24, 14, (170, 170, 170))

    if state["tempo_mensagem"] > 0:
        texto_centralizado(state["mensagem"], 80, 26, (217, 130, 43))

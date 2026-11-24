import random

import estado
from config import WORLD_W, WORLD_H, PHASES, CUTSCENES, ENEMY_TYPES, UPGRADES, TILES_DA_FASE
from mapas import obstaculos_da_fase, centro, INICIO
from audio import tocar_efeito
from cenas import abrir_cena
from historia import criar_historia_da_fase
from efeitos import criar_explosao
from utils import mostrar_mensagem, distancia
from jogador import criar_jogador, ganhar_xp
from itens import criar_itens_da_fase, soltar_cura
from recordes import salvar_recorde

state = estado.state


def novo_jogo():
    state["fase"] = 0
    state["score"] = 0
    state["melhorias"] = []
    state["niveis_pendentes"] = 0
    state["jogador"] = criar_jogador()
    abrir_cena("intro", "iniciar_fase")


def voltar_menu():
    state["recorde"] = salvar_recorde(state["score"])
    state["estado"] = "menu"


def iniciar_fase():
    state["inimigos"] = []
    state["tiros"] = []
    state["tiros_inimigos"] = []
    state["itens"] = []
    state["efeitos"] = []
    state["terminal"] = None
    state["dialogo"] = None
    state["encontro"] = None
    state["interagir"] = None
    state["obstaculos"] = []
    state["abates"] = 0
    state["boss_ativo"] = False
    state["filha"] = None
    state["tempo_spawn"] = 1

    state["marco"] = 0       # marco atual da fase (índice em PHASES[fase]["marcos"])
    state["marco_base"] = 0  # abates no começo do marco (para contar só os do marco atual)

    jogador = state["jogador"]
    jogador["x"], jogador["y"] = centro(INICIO)

    criar_chao()
    criar_obstaculos(jogador)
    criar_itens_da_fase()
    criar_historia_da_fase()
    state["estado"] = "jogo"
    mostrar_mensagem(PHASES[state["fase"]]["nome"])

    # melhorias ganhas ao derrotar o boss: escolhe agora, no começo da fase
    if state["niveis_pendentes"] > 0:
        state["opcoes"] = random.sample(range(len(UPGRADES)), 3)
        state["estado"] = "nivel"


def criar_chao():
    # sorteia um tile para cada quadradinho (80x80) do mapa
    tiles = TILES_DA_FASE[state["fase"]]
    state["chao"] = []
    for linha in range(WORLD_H // 80 + 1):
        linha_de_tiles = []
        for coluna in range(WORLD_W // 80 + 1):
            # 70% do chão usa o tile principal da fase; o resto varia só um pouco
            if random.random() < 0.7:
                linha_de_tiles.append(tiles[0])
            else:
                linha_de_tiles.append(random.choice(tiles))
        state["chao"].append(linha_de_tiles)


def criar_obstaculos(jogador):
    # layout fixo e desenhado à mão de cada fase (ver mapas.py)
    state["obstaculos"] = obstaculos_da_fase(state["fase"])


def progresso_do_marco():
    # devolve (atual, total, marco) do marco em andamento, ou None se todas as portas já abriram
    marcos = PHASES[state["fase"]]["marcos"]
    if state["marco"] >= len(marcos):
        return None
    marco = marcos[state["marco"]]
    if marco["tipo"] == "abates":
        atual = state["abates"] - state["marco_base"]
    elif marco["tipo"] == "pistas":
        atual = len([p for p in state["pistas"] if p["lida"]])
    else:
        atual = len([s for s in state["sobreviventes"] if s["falou"]])
    return min(atual, marco["n"]), marco["n"], marco


def atualizar_marcos():
    if state["boss_ativo"] or state["terminal"] or state["filha"]:
        return
    progresso = progresso_do_marco()
    if progresso and progresso[0] >= progresso[1]:
        abrir_porta(state["marco"])


def abrir_porta(indice):
    state["obstaculos"] = [b for b in state["obstaculos"] if b.get("porta") != indice]
    state["marco"] += 1
    state["marco_base"] = state["abates"]
    tocar_efeito("nivel")
    if state["marco"] >= len(PHASES[state["fase"]]["marcos"]):
        mostrar_mensagem("A última porta se abriu! O chefe espera...")
    else:
        mostrar_mensagem("Uma porta se abriu!")


def verificar_inimigos_derrotados():
    derrotados = [inimigo for inimigo in state["inimigos"] if inimigo["hp"] <= 0]

    for inimigo in derrotados:
        dados = ENEMY_TYPES[inimigo["tipo"]]
        tocar_efeito("explosao")
        criar_explosao(inimigo["x"], inimigo["y"], dados["boss"])
        state["score"] += dados["xp"] * 10
        if state["score"] > state["recorde"]:
            state["recorde"] = salvar_recorde(state["score"])
        ganhar_xp(dados["xp"])

        if dados["boss"]:
            terminar_fase(inimigo["x"], inimigo["y"])
            return

        state["abates"] += 1
        if random.random() < 0.12:
            soltar_cura(inimigo["x"], inimigo["y"])

    state["inimigos"] = [inimigo for inimigo in state["inimigos"] if inimigo["hp"] > 0]


def terminar_fase(x, y):
    fase_atual = PHASES[state["fase"]]
    state["inimigos"] = []
    state["tiros_inimigos"] = []

    if state["fase"] + 1 < len(PHASES):
        # o boss deixa um terminal com informações: Adam precisa ir até ele e apertar E
        state["terminal"] = {"tipo": "terminal", "x": x, "y": y, "cena": fase_atual["cena"]}
        mostrar_mensagem("Um terminal foi revelado! Aproxime-se e aperte E")
    else:
        # derrotou o Comandante: agora é achar a filha
        state["filha"] = {"x": WORLD_W / 2, "y": 90}
        mostrar_mensagem("O Comandante caiu! Encontre sua filha!")


def atualizar_filha():
    filha = state["filha"]
    if filha and distancia(filha, state["jogador"]) < 30:
        abrir_cena("fim", "menu")

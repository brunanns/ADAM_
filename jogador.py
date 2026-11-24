import math
import random

import estado
from PPlay.mouse import Mouse
from config import W, H, WORLD_W, WORLD_H, UPGRADES
from audio import tocar_efeito
from utils import dano_do_tiro, raio, distancia, mover, criar_tiro, bate_no_obstaculo, mostrar_mensagem

state = estado.state
_mouse = Mouse()


def criar_jogador():
    return {
        "x": WORLD_W / 2,
        "y": WORLD_H / 2,
        "hp": 100,
        "vida_max": 100,
        "velocidade": 150,
        "dano": 10,
        "tempo_tiro": 0,
        "recarga": 0.3,
        "direcao": 0,
        "andando": False,
        "anim_tempo": 0,
        "anim_frame": 0,
        "xp": 0,
        "nivel": 1,
        "xp_proximo": 20,
        "invencivel": 0,
    }


def atualizar_jogador(dt, teclado):
    jogador = state["jogador"]
    jogador["invencivel"] -= dt
    jogador["tempo_tiro"] -= dt
    mover_jogador(dt, teclado)
    atualizar_camera()
    atirar(teclado)
    atualizar_tiros_do_jogador(dt)


def mover_jogador(dt, teclado):
    jogador = state["jogador"]
    direita = teclado.key_pressed("d") or teclado.key_pressed("right")
    esquerda = teclado.key_pressed("a") or teclado.key_pressed("left")
    baixo = teclado.key_pressed("s") or teclado.key_pressed("down")
    cima = teclado.key_pressed("w") or teclado.key_pressed("up")

    dx = int(direita) - int(esquerda)
    dy = int(baixo) - int(cima)
    if dx != 0 or dy != 0:
        tamanho = math.hypot(dx, dy)  # evita andar mais rápido na diagonal
        passo_x = dx / tamanho * jogador["velocidade"] * dt
        passo_y = dy / tamanho * jogador["velocidade"] * dt
        mover(jogador, passo_x, passo_y, raio("adam"))

        # animação de caminhada: troca de quadro a cada 0.12 s
        jogador["andando"] = True
        jogador["anim_tempo"] += dt
        if jogador["anim_tempo"] >= 0.12:
            jogador["anim_tempo"] = 0
            jogador["anim_frame"] = (jogador["anim_frame"] + 1) % 4
    else:
        jogador["andando"] = False
        jogador["anim_frame"] = 0
        jogador["anim_tempo"] = 0


def atualizar_camera():
    jogador = state["jogador"]
    state["camera"][0] = max(0, min(WORLD_W - W, jogador["x"] - W / 2))
    state["camera"][1] = max(0, min(WORLD_H - H, jogador["y"] - H / 2))


def angulo_da_mira():
    # ângulo do Adam até o cursor do mouse (o mundo = tela + câmera)
    jogador = state["jogador"]
    mx, my = _mouse.get_position()
    alvo_x = mx + state["camera"][0]
    alvo_y = my + state["camera"][1]
    return math.atan2(alvo_y - jogador["y"], alvo_x - jogador["x"])


def atirar(teclado):
    jogador = state["jogador"]
    angulo = angulo_da_mira()
    # o sprite olha para o lado da mira (8 direções)
    jogador["direcao"] = round(angulo / (math.pi / 4)) % 8

    apertou = teclado.key_pressed("space") or _mouse.button_pressed(Mouse.LEFT)
    if apertou and jogador["tempo_tiro"] <= 0:
        jogador["tempo_tiro"] = jogador["recarga"]
        criar_tiro(state["tiros"], jogador["x"], jogador["y"], angulo, 480, jogador["dano"], 1.2)
        tocar_efeito("tiro")


def atualizar_tiros_do_jogador(dt):
    for tiro in state["tiros"]:
        tiro["x"] += tiro["vx"] * dt
        tiro["y"] += tiro["vy"] * dt
        tiro["tempo"] -= dt
        tiro["percorrido"] += math.hypot(tiro["vx"], tiro["vy"]) * dt

        if bate_no_obstaculo(tiro["x"], tiro["y"], 1):
            tiro["tempo"] = 0

        for inimigo in state["inimigos"]:
            if tiro["tempo"] > 0 and distancia(tiro, inimigo) < inimigo["raio"] + 3:
                inimigo["hp"] -= dano_do_tiro(tiro)
                tiro["tempo"] = 0

    state["tiros"] = [tiro for tiro in state["tiros"] if tiro["tempo"] > 0]


def machucar(dano):
    jogador = state["jogador"]
    if jogador["invencivel"] > 0:
        return

    jogador["hp"] -= dano
    jogador["invencivel"] = 0.4
    tocar_efeito("dano")
    if jogador["hp"] <= 0:
        jogador["hp"] = 0
        state["estado"] = "gameover"


def ganhar_xp(valor):
    jogador = state["jogador"]
    jogador["xp"] += valor
    subiu_de_nivel = False

    while jogador["xp"] >= jogador["xp_proximo"]:
        jogador["xp"] -= jogador["xp_proximo"]
        jogador["nivel"] += 1
        jogador["xp_proximo"] = round(jogador["xp_proximo"] * 1.4)
        state["niveis_pendentes"] += 1
        subiu_de_nivel = True

    if subiu_de_nivel:
        state["opcoes"] = random.sample(range(len(UPGRADES)), 3)
        state["estado"] = "nivel"
        tocar_efeito("nivel")


def aplicar_melhoria(indice, nivel=False):
    jogador = state["jogador"]

    if indice == 0:
        jogador["dano"] += 5
    elif indice == 1:
        jogador["vida_max"] += 20
        jogador["hp"] = min(jogador["vida_max"], jogador["hp"] + 30)
    elif indice == 2:
        jogador["velocidade"] += 20
    else:
        jogador["recarga"] *= 0.8

    nome = UPGRADES[indice].replace("+", "").split(" ")[0]
    state["melhorias"].append(nome)
    if nivel:
        state["niveis_pendentes"] -= 1
        if state["niveis_pendentes"] > 0:
            state["opcoes"] = random.sample(range(len(UPGRADES)), 3)
            state["estado"] = "nivel"
        else:
            state["estado"] = "jogo"
    return UPGRADES[indice]

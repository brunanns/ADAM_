import math
import random

import estado
from config import ENEMY_TYPES, PHASES
from mapas import SPAWNS, BOSS, centro, zona_da_posicao
from utils import raio, distancia, mover, criar_tiro, dano_do_tiro, mostrar_mensagem, bate_no_obstaculo
from jogador import machucar

state = estado.state


def criar_inimigo(tipo, x, y):
    dados = ENEMY_TYPES[tipo]
    state["inimigos"].append({
        "tipo": tipo,
        "x": x,
        "y": y,
        "hp": dados["hp"],
        "vida_max": dados["hp"],
        "estado": "parado",
        "recarga": random.random(),
        "raio": raio(dados["img"]),
        "anim_tempo": random.uniform(0, 0.3),
        "anim_frame": 0,
    })


def criar_inimigos_da_fase(dt):
    fase = PHASES[state["fase"]]
    state["tempo_spawn"] -= dt

    if state["boss_ativo"]:
        return

    if state["marco"] >= len(fase["marcos"]):
        # todas as portas abertas: hora do boss, na sala do chefe
        state["boss_ativo"] = True
        state["inimigos"] = []
        x, y = centro(BOSS)
        criar_inimigo(fase["boss"], x, y)
        mostrar_mensagem("BOSS: " + ENEMY_TYPES[fase["boss"]]["nome"])
    elif state["tempo_spawn"] <= 0 and len(state["inimigos"]) < 8:
        state["tempo_spawn"] = random.uniform(1, 2)
        ponto = escolher_ponto_de_spawn()
        tipo = random.choice(fase["pool"])
        criar_inimigo(tipo, ponto[0], ponto[1])


def escolher_ponto_de_spawn():
    # os inimigos só aparecem na zona em que Adam está (as portas fechadas separam as zonas)
    jogador = state["jogador"]
    zona = min(zona_da_posicao(jogador["y"]), 1)
    pontos = [centro(c) for c in SPAWNS[state["fase"]][zona]]
    longe = [p for p in pontos if math.hypot(p[0] - jogador["x"], p[1] - jogador["y"]) > 350]
    return random.choice(longe or pontos)


def atualizar_inimigos(dt):
    jogador = state["jogador"]

    for inimigo in state["inimigos"]:
        dados = ENEMY_TYPES[inimigo["tipo"]]
        d = distancia(inimigo, jogador)
        inimigo["recarga"] -= dt

        # estados: parado, perseguindo, atacando
        if d > 420:
            inimigo["estado"] = "parado"
        elif d > dados["alc"] * 0.8:
            inimigo["estado"] = "perseguindo"
        else:
            inimigo["estado"] = "atacando"

        if inimigo["estado"] == "perseguindo":
            perseguir(inimigo, dados, dt)
        if inimigo["estado"] == "atacando" and inimigo["recarga"] <= 0:
            inimigo["recarga"] = dados["rec"]
            atacar(inimigo, dados)

        # Animação: caminhada completa, idle mais lento e ataque em poses rápidas.
        inimigo["anim_tempo"] += dt
        if inimigo["estado"] == "perseguindo":
            intervalo = 0.13
            inicio, fim = 0, 3
        elif inimigo["estado"] == "atacando":
            intervalo = 0.11
            inicio, fim = 2, 3
        else:
            intervalo = 0.32
            inicio, fim = 0, 1
        if inimigo["anim_tempo"] >= intervalo:
            inimigo["anim_tempo"] = 0
            inimigo["anim_frame"] += 1
            if inimigo["anim_frame"] > fim or inimigo["anim_frame"] < inicio:
                inimigo["anim_frame"] = inicio

        # robô corpo a corpo machuca ao encostar
        if not dados["atira"] and d < inimigo["raio"] + raio("adam"):
            machucar(dados["dano"] * 0.5)

    separar_inimigos()


def perseguir(inimigo, dados, dt):
    jogador = state["jogador"]
    angulo = math.atan2(jogador["y"] - inimigo["y"], jogador["x"] - inimigo["x"])
    mover(inimigo, math.cos(angulo) * dados["vel"] * dt, math.sin(angulo) * dados["vel"] * dt, inimigo["raio"])


def atacar(inimigo, dados):
    jogador = state["jogador"]
    if not dados["atira"]:
        machucar(dados["dano"])
        return

    angulo = math.atan2(jogador["y"] - inimigo["y"], jogador["x"] - inimigo["x"])
    if dados["boss"]:
        direcoes = [0, -0.3, 0.3]  # boss atira 3 tiros
    else:
        direcoes = [0]
    for desvio in direcoes:
        criar_tiro(state["tiros_inimigos"], inimigo["x"], inimigo["y"], angulo + desvio, 220, dados["dano"], 2.5)


def atualizar_tiros_inimigos(dt):
    jogador = state["jogador"]

    for tiro in state["tiros_inimigos"]:
        tiro["x"] += tiro["vx"] * dt
        tiro["y"] += tiro["vy"] * dt
        tiro["tempo"] -= dt
        tiro["percorrido"] += math.hypot(tiro["vx"], tiro["vy"]) * dt

        if distancia(tiro, jogador) < raio("adam") + 4:
            machucar(dano_do_tiro(tiro))
            tiro["tempo"] = 0

        if bate_no_obstaculo(tiro["x"], tiro["y"], 1):
            tiro["tempo"] = 0

    state["tiros_inimigos"] = [tiro for tiro in state["tiros_inimigos"] if tiro["tempo"] > 0]


def separar_inimigos():
    # ninguém atravessa ninguém: se dois círculos se sobrepõem, empurra para fora
    jogador = state["jogador"]
    lista = state["inimigos"]

    for i in range(len(lista)):
        empurrar(lista[i], jogador, lista[i]["raio"], raio("adam"), 1)  # o Adam não é empurrado
        for j in range(i + 1, len(lista)):
            empurrar(lista[i], lista[j], lista[i]["raio"], lista[j]["raio"], 0.5)
            empurrar(lista[j], lista[i], lista[j]["raio"], lista[i]["raio"], 0.5)


def empurrar(a, b, raio_a, raio_b, parte):
    # empurra "a" para longe de "b" (parte = quanto da sobreposição "a" resolve)
    d = distancia(a, b)
    minimo = raio_a + raio_b - 1
    if d >= minimo:
        return

    if d == 0:
        ux, uy = 1, 0
    else:
        ux = (a["x"] - b["x"]) / d
        uy = (a["y"] - b["y"]) / d
    falta = (minimo - d) * parte
    mover(a, ux * falta, uy * falta, raio_a)

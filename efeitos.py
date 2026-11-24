import random

import estado

state = estado.state

TEMPO_POR_QUADRO = 0.07


def criar_explosao(x, y, grande=False):
    state["efeitos"].append({"x": x, "y": y, "tempo": 0})
    if grande:  # boss explode em vários pontos
        for _ in range(3):
            state["efeitos"].append({"x": x + random.randint(-25, 25), "y": y + random.randint(-25, 25), "tempo": -random.random() * 0.2})


def atualizar_efeitos(dt):
    for efeito in state["efeitos"]:
        efeito["tempo"] += dt
    state["efeitos"] = [e for e in state["efeitos"] if e["tempo"] < 4 * TEMPO_POR_QUADRO]


def quadro_da_explosao(efeito):
    return max(0, min(3, int(efeito["tempo"] / TEMPO_POR_QUADRO)))

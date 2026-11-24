import estado
from config import CUTSCENES

state = estado.state


def abrir_cena(nome, proxima_acao):
    state["estado"] = "cena"
    state["cena_nome"] = nome
    state["cena_lista"] = CUTSCENES[nome]
    state["cena_acao"] = proxima_acao

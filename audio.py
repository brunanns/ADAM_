import os

from PPlay.sound import Sound, Music

import estado
from config import MUSICAS, EFEITOS

state = estado.state

efeitos = {}
musica_atual = ""
musica_tocando = None


def tocar_efeito(nome):
    caminho = EFEITOS[nome]
    if not os.path.exists(caminho):
        return
    if nome not in efeitos:
        efeitos[nome] = Sound(caminho)
    efeitos[nome].play()


def escolher_musica():
    tela = state["estado"]
    if tela in ("menu", "ajuda", "gameover"):
        return "menu"
    if tela == "cena":
        return "cena"
    if state["boss_ativo"]:
        return "boss"
    return "fase" + str(state["fase"] + 1)


def atualizar_musica():
    # chamada a cada quadro: só troca a música quando a tela/fase muda
    global musica_atual, musica_tocando

    nome = escolher_musica()
    if nome == musica_atual:
        return
    musica_atual = nome

    if musica_tocando is not None:
        musica_tocando.stop(0)
        musica_tocando = None

    caminho = MUSICAS[nome]
    if os.path.exists(caminho):
        musica_tocando = Music(caminho)
        musica_tocando.play()

# ADAM v0.9 - menu cinematografico com sprite animado
import sys

from PPlay.window import Window

import audio
import estado
import game
import menu
from config import W, H


janela = Window(W, H, "Adam", intro=False)
teclado = janela.keyboard
estado.iniciar_janela(janela)
menu.iniciar()


while True:
    for event in janela.eventos:
        if event.type == 256:
            sys.exit()

    menu.handle_input(teclado)
    if estado.state["estado"] == "jogo":
        game.update(min(0.05, janela.delta_time()), teclado)

    audio.atualizar_musica()
    menu.draw()
    janela.update()

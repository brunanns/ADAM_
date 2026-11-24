import sys

import estado
import fases
import game
import historia
import jogador
from config import UPGRADES, W, H, CENA_IMAGENS
from utils import texto, texto_centralizado, desenhar_imagem_tela
from PPlay.gameimage import GameImage
from PPlay.mouse import Mouse


# Menu principal: todos os elementos são sprites independentes.
# O fundo é apenas cenário; Adam e os botões são desenhados separadamente.
_mouse = None
_fundo_menu = None
_botoes = []
_selecao_menu = 0
_menu_iniciado = False

OPCOES_MENU = [
    ("JOGAR", "jogar"),
    ("INSTRUÇÕES", "ajuda"),
    ("SAIR", "sair"),
]

BOTAO_X = 430
BOTAO_Y = 300
BOTAO_W = 340
BOTAO_H = 66
BOTAO_GAP = 12


def iniciar():
    """Carrega os sprites do menu depois que a janela PPlay existe."""
    global _mouse, _fundo_menu, _botoes, _menu_iniciado
    if _menu_iniciado:
        return

    _mouse = Mouse()
    _fundo_menu = GameImage("assets/menu_bg_v10.png")
    _botoes = [
        {
            "normal": GameImage("assets/menu/button_normal.png"),
            "selecionado": GameImage("assets/menu/button_selected.png"),
        }
        for _ in OPCOES_MENU
    ]
    _menu_iniciado = True


def _acao_opcao(indice):
    global _selecao_menu
    _selecao_menu = indice
    acao = OPCOES_MENU[indice][1]
    if acao == "jogar":
        fases.novo_jogo()
    elif acao == "ajuda":
        estado.state["estado"] = "ajuda"
    elif acao == "sair":
        sys.exit()


def _retangulo_botao(indice):
    y = BOTAO_Y + indice * (BOTAO_H + BOTAO_GAP)
    return BOTAO_X, y, BOTAO_W, BOTAO_H


def _atualizar_selecao_mouse():
    global _selecao_menu
    if _mouse is None:
        return
    mx, my = _mouse.get_position()
    for i in range(len(OPCOES_MENU)):
        x, y, w, h = _retangulo_botao(i)
        if x <= mx <= x + w and y <= my <= y + h:
            _selecao_menu = i
            if _mouse.button_down(1):
                _acao_opcao(i)
            return


def handle_input(teclado):
    global _selecao_menu
    tela = estado.state["estado"]

    if tela == "menu":
        _atualizar_selecao_mouse()
        if teclado.key_down("up") or teclado.key_down("w"):
            _selecao_menu = (_selecao_menu - 1) % len(OPCOES_MENU)
        elif teclado.key_down("down") or teclado.key_down("s"):
            _selecao_menu = (_selecao_menu + 1) % len(OPCOES_MENU)
        elif teclado.key_down("enter"):
            _acao_opcao(_selecao_menu)
        elif teclado.key_down("i"):
            estado.state["estado"] = "ajuda"
        elif teclado.key_down("esc"):
            sys.exit()

    elif tela == "ajuda":
        fechar = any(teclado.key_down(t) for t in ("i", "esc", "enter", "space", "backspace"))
        if fechar or (_mouse is not None and _mouse.button_down(1)):
            estado.state["estado"] = "menu"

    elif tela == "cena":
        if teclado.key_down("enter"):
            if estado.state["cena_acao"] == "iniciar_fase":
                fases.iniciar_fase()
            else:
                fases.voltar_menu()

    elif tela == "jogo":
        if teclado.key_down("p") or teclado.key_down("esc"):
            estado.state["estado"] = "pausa"

    elif tela == "pausa":
        if teclado.key_down("p") or teclado.key_down("esc"):
            estado.state["estado"] = "jogo"
        elif teclado.key_down("m"):
            fases.voltar_menu()

    elif tela == "nivel":
        for i in range(3):
            if teclado.key_down(str(i + 1)):
                jogador.aplicar_melhoria(estado.state["opcoes"][i], nivel=True)

    elif tela == "encontro":
        if teclado.key_down("e") or teclado.key_down("enter"):
            historia.fechar_encontro()

    elif tela == "gameover":
        if teclado.key_down("enter"):
            fases.voltar_menu()


def draw_menu_background():
    if _fundo_menu:
        _fundo_menu.set_position(0, 0)
        _fundo_menu.draw()


def _desenhar_botoes():
    for i, (rotulo, _) in enumerate(OPCOES_MENU):
        x, y, _, _ = _retangulo_botao(i)
        selecionado = i == _selecao_menu
        sprite = _botoes[i]["selecionado" if selecionado else "normal"]
        sprite.set_position(x, y)
        sprite.draw()
        cor = (225, 232, 211) if selecionado else (183, 184, 158)
        texto_centralizado(rotulo, y + 21, 22, cor, centro_x=x + BOTAO_W / 2)


def draw_main_menu():
    draw_menu_background()  # o título ADAM já faz parte da imagem de fundo

    _desenhar_botoes()

    
    texto_centralizado("W / S  SELECIONAR     ENTER  CONFIRMAR     I  INSTRUÇÕES", 535, 11, (125, 137, 119))


def draw_help():
    draw_menu_background()
    desenhar_imagem_tela("overlay", 0, 0)
    desenhar_imagem_tela("overlay", 0, 0)  # escurece bastante para o texto ler bem
    texto_centralizado("INSTRUÇÕES", 130, 36, (217, 205, 164))
    lines = [
        "WASD / Setas: mover",
        "MOUSE: mirar   |   CLIQUE ESQUERDO ou ESPAÇO: atirar",
        "P ou ESC: pausar",
        "Derrote robôs, ganhe XP e escolha melhorias (1, 2, 3)",
        "Cada fase termina com um boss. Permadeath!",
        "",
        "[I / ENTER / ESC] Voltar ao menu",
    ]
    for i, line in enumerate(lines):
        texto_centralizado(line, 210 + i * 32, 17, (207, 207, 184))


def draw_cutscene():
    desenhar_imagem_tela("cena_bg", 0, 0)
    imagem = CENA_IMAGENS.get(estado.state["cena_nome"])
    if imagem:
        desenhar_imagem_tela(imagem, 0, 30)  # ilustração da cena
        y_inicial, espaco = 235, 36
    else:
        y_inicial, espaco = 150, 42

    for i, line in enumerate(estado.state["cena_lista"]):
        if i == 0:
            color, size = (217, 130, 43), 26
        elif line.startswith("COORDENADA"):
            color, size = (91, 197, 190), 17
        else:
            color, size = (232, 232, 232), 17
        texto_centralizado(line, y_inicial + i * espaco, size, color)

    if estado.state["cena_acao"] == "menu":
        texto_centralizado("Pontos: %d" % estado.state["score"], 400, 20, (217, 130, 43))
    texto_centralizado("[ENTER] continuar", 505, 15, (136, 136, 136))


def draw_game_overlays():
    status = estado.state["estado"]
    if status in ("pausa", "nivel", "gameover", "encontro"):
        desenhar_imagem_tela("overlay", 0, 0)

    if status == "pausa":
        texto_centralizado("PAUSADO", 220, 44)
        texto_centralizado("[P] continuar   [M] menu", 290, 20)
    elif status == "nivel":
        texto_centralizado("NÍVEL %d! Escolha uma melhoria" % estado.state["jogador"]["nivel"], 170, 30, (70, 170, 255))
        for i, option in enumerate(estado.state["opcoes"]):
            desenhar_imagem_tela("card", 210, 240 + i * 56)
            texto_centralizado("[%d] %s" % (i + 1, UPGRADES[option]), 249 + i * 56, 22)
    elif status == "encontro":
        encontro = estado.state["encontro"]
        desenhar_imagem_tela("cena_sobreviventes", 0, 40)
        desenhar_imagem_tela("caixa_dialogo", 20, 225)
        texto(encontro["titulo"], 40, 237, 17, (91, 197, 190))
        for i, linha in enumerate(encontro["linhas"]):
            texto(linha, 40, 268 + i * 22, 15)
        texto_centralizado("[E] continuar", 372, 15, (136, 136, 136))
    elif status == "gameover":
        texto_centralizado("ADAM CAIU", 190, 52, (230, 50, 50))
        texto_centralizado("Permadeath: progresso perdido", 270, 20)
        texto_centralizado("Pontos: %d" % estado.state["score"], 305, 20)
        texto_centralizado("[ENTER] menu", 360, 20)


def draw():
    status = estado.state["estado"]
    if status == "menu":
        draw_main_menu()
    elif status == "ajuda":
        draw_help()
    elif status == "cena":
        draw_cutscene()
    else:
        game.draw()
        draw_game_overlays()

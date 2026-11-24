# Junta os módulos: jogador, inimigos, itens, fases e desenho
import efeitos
import historia
import estado
import desenho
import fases
import inimigos
import itens
import jogador

state = estado.state


def update(dt, teclado):
    state["tempo_mensagem"] -= dt
    jogador.atualizar_jogador(dt, teclado)
    inimigos.criar_inimigos_da_fase(dt)
    inimigos.atualizar_inimigos(dt)
    inimigos.atualizar_tiros_inimigos(dt)
    fases.verificar_inimigos_derrotados()
    fases.atualizar_marcos()
    itens.atualizar_itens()
    fases.atualizar_filha()
    historia.atualizar_historia(dt, teclado)
    efeitos.atualizar_efeitos(dt)


def draw():
    desenho.desenhar_jogo()

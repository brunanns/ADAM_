from PPlay.gameimage import GameImage

from config import IMAGE_NAMES
from recordes import carregar_recorde


# Tudo que muda durante o jogo fica aqui
state = {
    "estado": "menu",
    "fase": 0,
    "score": 0,
    "melhorias": [],
    "opcoes": [],
    "jogador": {},
    "inimigos": [],
    "tiros": [],
    "tiros_inimigos": [],
    "itens": [],
    "obstaculos": [],
    "camera": [0, 0],
    "abates": 0,
    "boss_ativo": False,
    "tempo_spawn": 1,
    "mensagem": "",
    "tempo_mensagem": 0,
    "filha": None,
    "recorde": carregar_recorde(),
    "niveis_pendentes": 0,
    "efeitos": [],
    "chao": [],
    "pistas": [],
    "sobreviventes": [],
    "terminal": None,
    "dialogo": None,
    "encontro": None,
    "interagir": None,
    "cena_nome": "",
}

janela = None
imagens = {}


def iniciar_janela(nova_janela):
    global janela
    janela = nova_janela
    for nome in IMAGE_NAMES:
        imagens[nome] = GameImage("assets/" + nome + ".png")

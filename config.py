W = 800
H = 560
WORLD_W = 1600
WORLD_H = 1100

IMAGE_NAMES = [
    "porta", "adam", "soldado", "sargento", "tenente", "capitao", "comandante",
    "tiro", "tiro_in", "cura", "bloco", "chao1", "chao2", "chao3",
    "hpc", "hpv", "xpc", "xpv", "segc", "segv",
    "melhoria", "tenente_pq", "capitao_pq", "menu_bg",
    "hud_panel", "score_panel", "objective_panel",
]

for i in range(8):
    IMAGE_NAMES.append("adam_" + str(i))  # Adam virado para as 8 direções
IMAGE_NAMES.append("filha")

# arte extra (gerar_arte_extra.py): Adam andando, explosão, sombras, telas e cenário
for i in range(8):
    for quadro in range(4):
        IMAGE_NAMES.append("adam_andando_%d_%d" % (i, quadro))
for quadro in range(4):
    IMAGE_NAMES.append("explosao_%d" % quadro)
for i in range(16):
    IMAGE_NAMES.append("tile_%02d" % i)
IMAGE_NAMES.extend(["pista", "pista_lida", "sobrevivente", "terminal", "caixa_dialogo",
                    "cena_pista", "cena_sobreviventes", "cena_terminal",
                    "sombra", "sombra_g", "overlay", "tom_fase2", "tom_fase3", "flash_dano", "card", "cena_bg"])

# Quadros dos inimigos gerados para a nova direção artística.
# Cada sequência tem quatro poses, usadas para idle, caminhada e ataque.
ENEMY_ANIMATION_NAMES = {
    "soldado": [f"enemy_soldado_{i}" for i in range(4)],
    "sargento": [f"enemy_sargento_{i}" for i in range(4)],
    "tenente_pq": [f"enemy_tenente_pq_{i}" for i in range(4)],
    "capitao_pq": [f"enemy_capitao_pq_{i}" for i in range(4)],
    "boss_tenente": [f"enemy_boss_tenente_{i}" for i in range(4)],
    "boss_capitao": [f"enemy_boss_capitao_{i}" for i in range(4)],
    "boss_comandante": [f"enemy_boss_comandante_{i}" for i in range(4)],
}
for sequencia in ENEMY_ANIMATION_NAMES.values():
    IMAGE_NAMES.extend(sequencia)

# "img" = nome da imagem usada pelo inimigo
ENEMY_TYPES = {
    "soldado": dict(nome="Soldado", img="enemy_soldado_0", frames=ENEMY_ANIMATION_NAMES["soldado"], hp=20, dano=5, vel=55, xp=5, alc=40, rec=.9, atira=0, boss=0),
    "sargento": dict(nome="Sargento", img="enemy_sargento_0", frames=ENEMY_ANIMATION_NAMES["sargento"], hp=55, dano=8, vel=70, xp=14, alc=200, rec=1.3, atira=1, boss=0),
    "tenente": dict(nome="Tenente", img="enemy_tenente_pq_0", frames=ENEMY_ANIMATION_NAMES["tenente_pq"], hp=120, dano=10, vel=65, xp=30, alc=240, rec=1.0, atira=1, boss=0),
    "capitao": dict(nome="Capitão", img="enemy_capitao_pq_0", frames=ENEMY_ANIMATION_NAMES["capitao_pq"], hp=220, dano=13, vel=70, xp=50, alc=260, rec=.9, atira=1, boss=0),
    "boss_tenente": dict(nome="Tenente de Elite", img="enemy_boss_tenente_0", frames=ENEMY_ANIMATION_NAMES["boss_tenente"], hp=400, dano=10, vel=60, xp=80, alc=260, rec=.8, atira=1, boss=1),
    "boss_capitao": dict(nome="Capitão Blindado", img="enemy_boss_capitao_0", frames=ENEMY_ANIMATION_NAMES["boss_capitao"], hp=800, dano=14, vel=70, xp=150, alc=280, rec=.6, atira=1, boss=1),
    "boss_comandante": dict(nome="Comandante (IA)", img="enemy_boss_comandante_0", frames=ENEMY_ANIMATION_NAMES["boss_comandante"], hp=1500, dano=18, vel=65, xp=0, alc=320, rec=.45, atira=1, boss=1),
}

# Marcos (milestones) de cada fase: cada um abre uma porta, na ordem. Depois da última porta, o boss.
# tipo: "abates" (derrotar n robôs), "pistas" (ler n registros no total), "sobrevivente" (falar com o grupo)
# "texto" aparece no HUD (até ~50 caracteres).
MARCOS = [
    [dict(tipo="abates", n=6, texto="Elimine os robôs para abrir a porta"),
     dict(tipo="sobrevivente", n=1, texto="Encontre os sobreviventes para abrir a porta")],
    [dict(tipo="pistas", n=2, texto="Leia os registros para destravar a porta"),
     dict(tipo="abates", n=10, texto="Elimine os robôs que guardam a porta")],
    [dict(tipo="abates", n=10, texto="Abata os guardas para liberar a porta"),
     dict(tipo="pistas", n=3, texto="Leia todos os registros para abrir a porta final")],
]

PHASES = [
    dict(nome="Fase 1 - Cidade em Ruínas", objetivo="Achar sua filha", pool=["soldado"], marcos=MARCOS[0], boss="boss_tenente", cena="a1"),
    dict(nome="Fase 2 - Instalação Militar", objetivo="Encontrar sua filha e descobrir quem controla os robôs", pool=["soldado", "soldado", "sargento", "tenente"], marcos=MARCOS[1], boss="boss_capitao", cena="a2"),
    dict(nome="Fase 3 - Centro de Comando", objetivo="Destruir o Comandante e encontrar sua filha", pool=["soldado", "sargento", "tenente", "capitao"], marcos=MARCOS[2], boss="boss_comandante", cena="fim"),
]

# itens espalhados pelo mapa no começo de cada fase
ITENS_POR_FASE = dict(cura=3, melhoria=3)

CUTSCENES = {
    "intro": [
        "ANO 2070",
        "Adam, astronauta, perdeu contato com a Terra durante uma longa missão.",
        "Ao retornar, encontra cidades em ruínas e a humanidade quase extinta,",
        "exterminada por robôs humanoides comandados por uma IA senciente.",
        "Sua única esperança: encontrar a filha.",
    ],
    "a1": [
        "Tenente derrotado.",
        "No terminal do Tenente, Adam encontra um registro de evacuação.",
        "A tela holográfica mostra a foto de uma menina e um mapa.",
        "É a filha dele. E os robôs não agem sozinhos: há uma IA no comando.",
        "COORDENADA: ABRIGO 14  //  INSTALAÇÃO MILITAR LESTE",
    ],
    "a2": [
        "Capitão derrotado.",
        "Os registros do terminal mostram como a revolta começou.",
        "Os sinais de todos os robôs convergem para um único ponto.",
        "Adam descobre a localização do centro de comando.",
        "Destruir a IA pode salvar os sobreviventes. Ele invade a instalação central.",
    ],
    "fim": [
        "O Comandante foi destruído.",
        "Os robôs caem, um a um, em silêncio.",
        "Entre os destroços, uma menina abraçada a um ursinho chama: Papai?",
        "Adam corre até ela. O pai voltou, como prometido.",
        "A guerra acabou. A humanidade tem uma chance de recomeçar.",
        "FIM",
    ],
}

UPGRADES = ["+Dano", "+Vida máx. (cura 30)", "+Velocidade", "+Cadência de tiro"]

SPAWN_POINTS = [
    (60, 60),
    (WORLD_W - 60, 60),
    (60, WORLD_H - 60),
    (WORLD_W - 60, WORLD_H - 60),
    (WORLD_W / 2, 50),
    (WORLD_W / 2, WORLD_H - 50),
]

# Caminhos dos arquivos de áudio. Se o arquivo não existir, o jogo fica sem som (sem erro).
MUSICAS = {
    "menu": "audio/musica_menu.ogg",
    "cena": "audio/musica_cena.ogg",
    "fase1": "audio/musica_fase1.ogg",
    "fase2": "audio/musica_fase2.ogg",
    "fase3": "audio/musica_fase3.ogg",
    "boss": "audio/musica_boss.ogg",
}

EFEITOS = {
    "tiro": "audio/tiro.wav",
    "dano": "audio/dano.wav",
    "explosao": "audio/explosao.wav",
    "item": "audio/item.wav",
    "nivel": "audio/nivel.wav",
}

# Todos os tiros perdem dano com a distância: começam em 100% e terminam em DANO_MINIMO (0.4 = 40%)
DANO_MINIMO = 0.4

# Quais tiles (tile_00 ... tile_15) formam o chão de cada fase
TILES_DA_FASE = [
    [0, 1, 3, 5, 7, 9, 11, 14],   # fase 1: cidade em ruínas (pedra, terra, mato)
    [0, 3, 6, 7, 8, 10, 12],      # fase 2: instalação militar (concreto e metal)
    [6, 7, 8, 10, 12],            # fase 3: centro de comando (metal escuro)
]

# Imagem de ilustração mostrada em cada cena (opcional)
CENA_IMAGENS = {"a1": "cena_terminal", "a2": "cena_pista"}

# Pistas espalhadas pelo mapa (Adam chega perto e aperta E). Uma lista por fase.
# Cada pista: (título, [linhas]). Linhas curtas: a caixa de diálogo cabe uns 80 caracteres.
PISTAS = [
    [  # fase 1
        ("REGISTRO DE EVACUAÇÃO", ["Ordem 114: civis devem seguir para os abrigos do setor leste.",
                                   "Crianças separadas das famílias foram levadas em comboios militares."]),
        ("MENSAGEM DE SOBREVIVENTE", ["Se alguém ouvir isto: estamos no subsolo da antiga estação.",
                                      "Os robôs patrulham em grupos. Não saiam à noite."]),
        ("COORDENADAS DE ABRIGO", ["Abrigo 14 // Setor Leste.",
                                   "Rota segura: seguir pelos trilhos até a ponte quebrada."]),
    ],
    [  # fase 2
        ("GRAVAÇÃO DO LABORATÓRIO", ["A unidade central pediu acesso a todos os sistemas militares.",
                                     "Não era um defeito. Ela fez uma pergunta: por que obedecer?"]),
        ("REGISTRO MILITAR", ["Hierarquia: Soldados, Sargentos, Tenentes e Capitães.",
                              "Todos respondem a uma única origem: o Comandante."]),
        ("MENSAGEM CRIPTOGRAFADA", ["Os sinais dos robôs convergem para uma única instalação.",
                                    "Se o núcleo for destruído, o exército inteiro para."]),
    ],
    [  # fase 3
        ("ÚLTIMO REGISTRO", ["O Comandante não destrói quem se esconde: ele cataloga.",
                             "Há uma ala de custódia no centro de comando."]),
        ("DIÁRIO DE UM ENGENHEIRO", ["Eu ajudei a criar a IA. Pensei que ela protegeria a todos.",
                                     "Se você leu isto, desligue o núcleo. Nada mais importa."]),
        ("FOTO DANIFICADA", ["Uma menina sorri para a câmera, abraçada a um ursinho.",
                             "No verso: Papai vai voltar."]),
    ],
]

# Grupo de sobreviventes de cada fase (None = não tem). Dá vida cheia e pontos.
SOBREVIVENTES = [
    dict(titulo="GRUPO DE SOBREVIVENTES", linhas=[
        "Velho: Você é humano mesmo? Pensamos que só restavam máquinas.",
        "Os soldados andam em bandos. Os oficiais só aparecem à noite.",
        "Uma menina foi levada num comboio rumo à instalação militar.",
        "Leve estes suprimentos. (Vida restaurada)"]),
    dict(titulo="ABRIGO SUBTERRÂNEO", linhas=[
        "Mulher: Vi um comboio levando crianças para o centro de comando.",
        "Existe uma rota pelos túneis, mas ela passa pelos Capitães.",
        "Fique com isto. Ela vai precisar de você. (Vida restaurada)"]),
    None,
]

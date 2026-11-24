# Layouts fixos das fases. Coordenadas em CÉLULAS de 40x40 px (mapa = 40 colunas x 27 linhas).
# Cada fase tem 3 zonas empilhadas, separadas por paredes com uma PORTA:
#   zona 0 (linhas 19-26): onde Adam começa     -> porta 0 (linha 18)
#   zona 1 (linhas 10-17): meio do mapa         -> porta 1 (linha 9)
#   zona 2 (linhas 0-8)  : sala do chefe
# As portas só abrem quando o marco da fase é cumprido (ver "marcos" em config.py).
# Bloco/porta: (coluna, linha, largura, altura).

CELULA = 40
INICIO = (20, 22)   # célula onde Adam começa
BOSS = (20, 2)      # célula onde o chefe nasce

# paredes + cobertura de cada fase
LAYOUTS = [[[0, 18, 18, 1], [22, 18, 18, 1], [0, 9, 18, 1], [22, 9, 18, 1], [5, 21, 5, 3], [30, 21, 5, 3], [6, 12, 5, 3], [29, 12, 5, 3], [13, 15, 3, 2], [24, 15, 3, 2], [8, 3, 2, 2], [30, 3, 2, 2], [12, 6, 2, 2], [26, 6, 2, 2]],
    [[0, 18, 4, 1], [8, 18, 32, 1], [0, 9, 32, 1], [36, 9, 4, 1], [12, 21, 1, 4], [27, 21, 1, 4], [30, 22, 3, 2], [10, 12, 4, 3], [20, 14, 1, 4], [26, 11, 5, 3], [6, 4, 2, 2], [12, 6, 2, 2], [26, 6, 2, 2], [30, 3, 2, 2]],
    [[0, 18, 32, 1], [36, 18, 4, 1], [0, 9, 4, 1], [8, 9, 32, 1], [6, 21, 2, 2], [12, 23, 2, 2], [26, 23, 2, 2], [32, 21, 2, 2], [10, 11, 2, 2], [16, 14, 2, 2], [24, 11, 2, 2], [30, 14, 2, 2], [6, 15, 2, 2], [14, 3, 1, 4], [25, 3, 1, 4], [8, 6, 2, 2], [30, 6, 2, 2]]]

# as duas portas de cada fase (porta 0, porta 1)
PORTAS = [[[18, 18, 4, 1], [18, 9, 4, 1]], [[4, 18, 4, 1], [32, 9, 4, 1]], [[32, 18, 4, 1], [4, 9, 4, 1]]]

# pontos de spawn de inimigos: SPAWNS[fase][zona]
SPAWNS = [[[[2, 21], [37, 21], [2, 24], [37, 24]], [[2, 13], [37, 13]]], [[[37, 21], [2, 24], [37, 24]], [[2, 13], [37, 14]]], [[[2, 21], [2, 24], [37, 24]], [[37, 13], [2, 13]]]]

# Posições fixas (coluna, linha) de pistas, sobrevivente e itens, por fase
POSICOES = [{'cura': [[12, 21], [20, 13], [20, 7]],
  'melhoria': [[28, 24], [4, 16], [36, 11]],
  'pistas': [[3, 22], [9, 16], [34, 16]],
  'sobrevivente': [30, 16]},
 {'cura': [[29, 25], [30, 16], [20, 7]],
  'melhoria': [[6, 23], [8, 16], [34, 12]],
  'pistas': [[16, 22], [32, 25], [24, 16]],
  'sobrevivente': [16, 12]},
 {'cura': [[30, 24], [20, 16], [20, 7]],
  'melhoria': [[4, 23], [26, 16], [8, 12]],
  'pistas': [[16, 22], [13, 13], [34, 12]],
  'sobrevivente': None}]


def obstaculos_da_fase(fase):
    blocos = []
    for (c, r, w, h) in LAYOUTS[fase]:
        blocos.append({"x": c * CELULA, "y": r * CELULA, "nx": w, "ny": h, "w": w * CELULA, "h": h * CELULA})
    for indice, (c, r, w, h) in enumerate(PORTAS[fase]):
        blocos.append({"x": c * CELULA, "y": r * CELULA, "nx": w, "ny": h, "w": w * CELULA, "h": h * CELULA, "porta": indice})
    return blocos


def zona_da_posicao(y):
    # 0 = início, 1 = meio, 2 = sala do chefe (y em pixels)
    if y >= 19 * CELULA:
        return 0
    if y >= 10 * CELULA:
        return 1
    return 2


def centro(celula):
    # centro da célula em pixels
    return celula[0] * CELULA + CELULA / 2, celula[1] * CELULA + CELULA / 2

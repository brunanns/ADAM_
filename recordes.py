from pathlib import Path


ARQUIVO_RECORDES = Path(__file__).with_name("recordes.txt")


def carregar_recorde():
    try:
        conteudo = ARQUIVO_RECORDES.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        return 0

    if not conteudo:
        return 0

    try:
        return max(0, int(conteudo))
    except ValueError:
        return 0  # texto estranho no arquivo: começa do zero


def salvar_recorde(recorde):
    recorde = max(recorde, carregar_recorde())
    ARQUIVO_RECORDES.write_text(str(recorde) + "\n", encoding="utf-8")
    return recorde

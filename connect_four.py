import FreeSimpleGUI as sg

# Estrutura e Constantes

# Dimensões do Tabuleiro
LINHAS = 6
COLUNAS = 7
VAZIO = "-"
JOGADOR_1 = "X"
JOGADOR_2 = "O"


def criar_tabuleiro():
    """Cria um tabuleiro 6x7 inicialmente vazio."""
    return [[VAZIO for _ in range(COLUNAS)] for _ in range(LINHAS)]

# Regra de Gravidade

def aplicar_jogada(tabuleiro, coluna, jogador):
    """Aplica a regra de gravidade: insere a peça na linha mais baixa disponível da coluna."""
    for linha in range(LINHAS - 1, -1, -1):
        if tabuleiro[linha][coluna] == VAZIO:
            tabuleiro[linha][coluna] = jogador
            return linha, "continua"
    return None, "coluna_cheia"

# Detecção de Vitória e Empate

def verificar_vitoria(tabuleiro, linha, coluna, jogador):
    """Verifica se há 4 peças alinhadas na horizontal, vertical ou diagonais."""
    # Horizontal
    for c in range(COLUNAS - 3):
        if (
            tabuleiro[linha][c] == jogador
            and tabuleiro[linha][c + 1] == jogador
            and tabuleiro[linha][c + 2] == jogador
            and tabuleiro[linha][c + 3] == jogador
        ):
            return True

    # Vertical
    for r in range(LINHAS - 3):
        if (
            tabuleiro[r][coluna] == jogador
            and tabuleiro[r + 1][coluna] == jogador
            and tabuleiro[r + 2][coluna] == jogador
            and tabuleiro[r + 3][coluna] == jogador
        ):
            return True

    # Diagonal Positiva (/)
    for r in range(3, LINHAS):
        for c in range(COLUNAS - 3):
            if (
                tabuleiro[r][c] == jogador
                and tabuleiro[r - 1][c + 1] == jogador
                and tabuleiro[r - 2][c + 2] == jogador
                and tabuleiro[r - 3][c + 3] == jogador
            ):
                return True

    # Diagonal Negativa (\)
    for r in range(LINHAS - 3):
        for c in range(COLUNAS - 3):
            if (
                tabuleiro[r][c] == jogador
                and tabuleiro[r + 1][c + 1] == jogador
                and tabuleiro[r + 2][c + 2] == jogador
                and tabuleiro[r + 3][c + 3] == jogador
            ):
                return True

    return False


def tabuleiro_cheio(tabuleiro):
    """Verifica se o tabuleiro está completamente preenchido (empate)."""
    return all(tabuleiro[0][c] != VAZIO for c in range(COLUNAS))


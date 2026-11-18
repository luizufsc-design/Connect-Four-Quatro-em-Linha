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
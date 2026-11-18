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


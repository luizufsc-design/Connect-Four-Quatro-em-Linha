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

# Interface Gráfica com FreeSimpleGUI

def executar_interface():
    """Executa o jogo Connect Four utilizando FreeSimpleGUI."""
    sg.theme("DarkBlue")

    # Layout da grade de botões representando o tabuleiro
    layout = [
        [
            sg.Text(
                "Connect Four - Quatro em Linha",
                font=("Helvetica", 16, "bold"),
                justification="center",
                expand_x=True,
            )
        ],
        [
            sg.Text(
                "Vez do Jogador: X",
                key="-STATUS-",
                font=("Helvetica", 12),
                justification="center",
                expand_x=True,
            )
        ],
    ]

    # Botões do tabuleiro (6 linhas x 7 colunas)
    grid_layout = []
    for r in range(LINHAS):
        linha_botoes = []
        for c in range(COLUNAS):
            linha_botoes.append(
                sg.Button(
                    VAZIO,
                    size=(4, 2),
                    key=(r, c),
                    font=("Helvetica", 12, "bold"),
                    button_color=("white", "gray25"),
                )
            )
        grid_layout.append(linha_botoes)

    layout.append([sg.Column(grid_layout, justification="center")])
    layout.append(
        [
            sg.Button(
                "Reiniciar",
                key="-RESTART-",
                font=("Helvetica", 10),
                expand_x=True,
            ),
            sg.Button("Sair", key="-EXIT-", font=("Helvetica", 10), expand_x=True),
        ]
    )

    window = sg.Window("Connect Four", layout, finalize=True)

    tabuleiro = criar_tabuleiro()
    jogador_atual = JOGADOR_1
    jogo_encerrado = False

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == "-EXIT-":
            break

        if event == "-RESTART-":
            tabuleiro = criar_tabuleiro()
            jogador_atual = JOGADOR_1
            jogo_encerrado = False
            window["-STATUS-"].update(f"Vez do Jogador: {jogador_atual}")
            for r in range(LINHAS):
                for c in range(COLUNAS):
                    window[(r, c)].update(
                        VAZIO, button_color=("white", "gray25")
                    )
            continue

        if jogo_encerrado:
            continue

        # Verifica se o clique ocorreu em um dos botões do tabuleiro (coordenada tupla)
        if isinstance(event, tuple):
            _, col_clicada = event
            linha_livre, status = aplicar_jogada(
                tabuleiro, col_clicada, jogador_atual
            )

            if status == "coluna_cheia":
                sg.popup_error(
                    "Coluna cheia! Escolha outra coluna.", title="Aviso"
                )
                continue

            # Atualiza o botão visual correspondente
            cor_peca = "firebrick3" if jogador_atual == JOGADOR_1 else "gold2"
            window[(linha_livre, col_clicada)].update(
                jogador_atual, button_color=("white", cor_peca)
            )

            # Verifica vitória
            if verificar_vitoria(
                tabuleiro, linha_livre, col_clicada, jogador_atual
            ):
                window["-STATUS-"].update(
                    f"🎉 Jogador {jogador_atual} venceu a partida!"
                )
                sg.popup_ok(
                    f"Fim de jogo! O Jogador {jogador_atual} venceu!",
                    title="Vitória!",
                )
                jogo_encerrado = True
                continue

            # Verifica empate
            if tabuleiro_cheio(tabuleiro):
                window["-STATUS-"].update("Empate! O tabuleiro está cheio.")
                sg.popup_ok("Fim de jogo! Deu empate!", title="Empate")
                jogo_encerrado = True
                continue

            # Alterna o turno
            jogador_atual = (
                JOGADOR_2 if jogador_atual == JOGADOR_1 else JOGADOR_1
            )
            window["-STATUS-"].update(f"Vez do Jogador: {jogador_atual}")

    window.close()


if __name__ == "__main__":
    executar_interface()
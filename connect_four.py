import FreeSimpleGUI as sg
import random

# Estrutura e Constantes
# Dimensões do Tabuleiro padrão do Connect Four
LINHAS = 6
COLUNAS = 7
VAZIO = "-"
JOGADOR_1 = "X"
JOGADOR_2 = "O"

def criar_tabuleiro():
    """Cria um tabuleiro 6x7 inicialmente vazio."""
    return [[VAZIO for _ in range(COLUNAS)] for _ in range(LINHAS)]

def aplicar_jogada(tabuleiro, coluna, jogador):
    """Aplica a regra de gravidade: insere a peça na linha mais baixa disponível da coluna."""
    for linha in range(LINHAS - 1, -1, -1):
        if tabuleiro[linha][coluna] == VAZIO:
            tabuleiro[linha][coluna] = jogador
            return linha, "continua"
    return None, "coluna_cheia"

def verificar_vitoria(tabuleiro, linha, coluna, jogador):
    """Verifica se há 4 peças alinhadas na horizontal, vertical ou diagonais."""
    # Horizontal
    for c in range(COLUNAS - 3):
        if (tabuleiro[linha][c] == jogador and 
            tabuleiro[linha][c + 1] == jogador and 
            tabuleiro[linha][c + 2] == jogador and 
            tabuleiro[linha][c + 3] == jogador):
            return True

    # Vertical
    for r in range(LINHAS - 3):
        if (tabuleiro[r][coluna] == jogador and 
            tabuleiro[r + 1][coluna] == jogador and 
            tabuleiro[r + 2][coluna] == jogador and 
            tabuleiro[r + 3][coluna] == jogador):
            return True

    # Diagonal Principal (descendente)
    for r in range(LINHAS - 3):
        for c in range(COLUNAS - 3):
            if (tabuleiro[r][c] == jogador and 
                tabuleiro[r + 1][c + 1] == jogador and 
                tabuleiro[r + 2][c + 2] == jogador and 
                tabuleiro[r + 3][c + 3] == jogador):
                return True

    # Diagonal Secundária (ascendente)
    for r in range(3, LINHAS):
        for c in range(COLUNAS - 3):
            if (tabuleiro[r][c] == jogador and 
                tabuleiro[r - 1][c + 1] == jogador and 
                tabuleiro[r - 2][c + 2] == jogador and 
                tabuleiro[r - 3][c + 3] == jogador):
                return True

    return False

def tabuleiro_cheio(tabuleiro):
    """Verifica se o tabuleiro está totalmente preenchido (empate)."""
    return all(tabuleiro[0][c] != VAZIO for c in range(COLUNAS))

def jogada_computador(tabuleiro):
    """Escolhe uma coluna válida aleatoriamente para o computador."""
    colunas_validas = [c for c in range(COLUNAS) if tabuleiro[0][c] == VAZIO]
    return random.choice(colunas_validas) if colunas_validas else None

def atualizar_interface(janela, tabuleiro):
    """Atualiza visualmente os botões do tabuleiro na interface gráfica."""
    for r in range(LINHAS):
        for c in range(COLUNAS):
            valor = tabuleiro[r][c]
            cor = "white"
            if valor == JOGADOR_1:
                cor = "red"
            elif valor == JOGADOR_2:
                cor = "blue"
            janela[(r, c)].update(text=valor, button_color=('black', cor))

def main():
    sg.theme('LightBlue2')

    # Layout inicial com seleção de modo de jogo
    layout = [
        [sg.Text("Connect Four (Quatro em Linha)", font=("Helvetica", 16, "bold"), justification="center", expand_x=True)],
        [sg.Text("Escolha o modo de jogo:"), 
         sg.Combo(["Humano x Humano", "Humano x Computador"], default_value="Humano x Humano", key="-MODO-", readonly=True, enable_events=True),
         sg.Button("Reiniciar Jogo", key="-REINICIAR-")],
        [sg.HorizontalSeparator()],
        # Grade do tabuleiro com botões interativos para cada coluna/linha
        [[sg.Button(VAZIO, size=(4, 2), key=(r, c), font=("Helvetica", 12, "bold")) for c in range(COLUNAS)] for r in range(LINHAS)],
        [sg.HorizontalSeparator()],
        [sg.Text("Vez do Jogador: X (Vermelho)", key="-STATUS-", font=("Helvetica", 12, "bold"), expand_x=True, justification="center")],
        [sg.Button("Sair", font=("Helvetica", 10))]
    ]

    janela = sg.Window("Connect Four", layout, finalize=True)

    tabuleiro = criar_tabuleiro()
    turno = JOGADOR_1  # Jogador 1 começa (X)
    jogo_encerrado = False

    while True:
        evento, valores = janela.read()

        if evento == sg.WIN_CLOSED or evento == "Sair":
            break

        if evento == "-REINICIAR-" or evento == "-MODO-":
            tabuleiro = criar_tabuleiro()
            turno = JOGADOR_1
            jogo_encerrado = False
            atualizar_interface(janela, tabuleiro)
            janela["-STATUS-"].update(f"Vez do Jogador: {turno} ({'Vermelho' if turno == JOGADOR_1 else 'Azul'})")
            continue

        if jogo_encerrado:
            continue

        # Verifica se o clique veio de um botão do tabuleiro (coordenada em tupla)
        if isinstance(evento, tuple):
            r_clicado, c_clicado = evento

            # Aplica a jogada na coluna clicada
            linha, status = aplicar_jogada(tabuleiro, c_clicado, turno)

            if status == "coluna_cheia":
                sg.popup_ok("Esta coluna está cheia! Escolha outra.", title="Aviso")
                continue

            atualizar_interface(janela, tabuleiro)

            # Verifica condição de vitória
            if verificar_vitoria(tabuleiro, linha, c_clicado, turno):
                cor_vencedor = "Vermelho (X)" if turno == JOGADOR_1 else "Azul (O)"
                sg.popup_ok(f"Fim de jogo! O Jogador {turno} ({cor_vencedor}) venceu!", title="Vitória!")
                janela["-STATUS-"].update(f"Vencedor: Jogador {turno}!")
                jogo_encerrado = True
                continue

            # Verifica condição de empate
            if tabuleiro_cheio(tabuleiro):
                sg.popup_ok("Fim de jogo! O tabuleiro está cheio. Empate!", title="Empate")
                janela["-STATUS-"].update("Fim de jogo: Empate!")
                jogo_encerrado = True
                continue

            # Alterna o turno
            if valores["-MODO-"] == "Humano x Humano":
                turno = JOGADOR_2 if turno == JOGADOR_1 else JOGADOR_1
                janela["-STATUS-"].update(f"Vez do Jogador: {turno} ({'Vermelho' if turno == JOGADOR_1 else 'Azul'})")
            else:
                # Modo Humano x Computador
                # Jogador 1 (Humano) joga, agora entra o Computador (JOGADOR_2)
                turno = JOGADOR_2
                janela["-STATUS-"].update("Vez do Computador (O)...")
                janela.refresh()

                # Pequena pausa dramática para a jogada da IA
                import time
                time.sleep(0.5)

                c_comp = jogada_computador(tabuleiro)
                if c_comp is not None:
                    linha_comp, _ = aplicar_jogada(tabuleiro, c_comp, JOGADOR_2)
                    atualizar_interface(janela, tabuleiro)

                    if verificar_vitoria(tabuleiro, linha_comp, c_comp, JOGADOR_2):
                        sg.popup_ok("Fim de jogo! O Computador venceu!", title="Fim de Jogo")
                        janela["-STATUS-"].update("Computador venceu!")
                        jogo_encerrado = True
                        continue

                    if tabuleiro_cheio(tabuleiro):
                        sg.popup_ok("Fim de jogo! Empate!", title="Empate")
                        janela["-STATUS-"].update("Empate!")
                        jogo_encerrado = True
                        continue

                # Retorna a vez para o Humano
                turno = JOGADOR_1
                janela["-STATUS-"].update(f"Vez do Jogador: {turno} (Vermelho)")

    janela.close()

if __name__ == "__main__":
    main()
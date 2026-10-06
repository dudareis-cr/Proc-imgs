# -*- coding: utf-8 -*-
"""
Filtro de mediana seletivo para imagens PGM (formato P2 / ASCII).

Ideia: para cada pixel, calcula a mediana da janela 3x3 ao redor dele.
Só substitui o pixel pela mediana se ele for MUITO diferente dela
(diferença maior que LIMITE). Assim, pixels normais não são alterados
e só o ruído (valores muito distoantes) é corrigido.

Uso: coloque a imagem na mesma pasta deste arquivo, ajuste os nomes
abaixo e execute:  python filtro_mediana.py
"""

# ====== CONFIGURAÇÕES (altere aqui) ======
ARQUIVO_ENTRADA = "glassware_noisy.ascii.pgm"   # imagem original (P2)
ARQUIVO_SAIDA = "saida.pgm"       # imagem filtrada que será criada
LIMITE = 20                       # margem: diferença mínima para considerar ruído
# =========================================


def ler_pgm(nome):
    """Lê um PGM P2 e devolve (largura, altura, maximo, matriz)."""
    with open(nome, "r") as f:
        # Remove comentários (tudo depois de '#') e junta todos os números
        texto = ""
        for linha in f:
            texto += linha.split("#")[0] + " "
    dados = texto.split()

    if dados[0] != "P2":
        raise ValueError("Este programa só lê PGM no formato P2 (ASCII).")

    largura = int(dados[1])
    altura = int(dados[2])
    maximo = int(dados[3])
    valores = [int(v) for v in dados[4:4 + largura * altura]]

    # Transforma a lista em matriz (lista de linhas)
    matriz = []
    for i in range(altura):
        matriz.append(valores[i * largura:(i + 1) * largura])
    return largura, altura, maximo, matriz


def mediana(lista):
    """Mediana: ordena e pega o valor do meio (ou média dos dois do meio)."""
    lista = sorted(lista)
    n = len(lista)
    meio = n // 2
    if n % 2 == 1:
        return lista[meio]
    return (lista[meio - 1] + lista[meio]) // 2


def filtrar(matriz, largura, altura, limite):
    """Aplica o filtro de mediana 3x3 só nos pixels muito distoantes."""
    # Cópia da matriz: lemos da original e escrevemos na cópia,
    # para que pixels já corrigidos não influenciem os próximos.
    resultado = [linha[:] for linha in matriz]
    alterados = 0

    for y in range(altura):
        for x in range(largura):
            # Monta a janela 3x3 (nas bordas, usa só os vizinhos que existem)
            janela = []
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < altura and 0 <= nx < largura:
                        janela.append(matriz[ny][nx])

            med = mediana(janela)

            # Só troca se o pixel for muito diferente da mediana
            if abs(matriz[y][x] - med) > limite:
                resultado[y][x] = med
                alterados += 1

    return resultado, alterados


def salvar_pgm(nome, largura, altura, maximo, matriz):
    """Grava a matriz em um arquivo PGM P2."""
    with open(nome, "w") as f:
        f.write("P2\n")
        f.write(f"{largura} {altura}\n")
        f.write(f"{maximo}\n")
        for linha in matriz:
            f.write(" ".join(str(v) for v in linha) + "\n")


# ---------------- Programa principal ----------------
largura, altura, maximo, imagem = ler_pgm(ARQUIVO_ENTRADA)
filtrada, qtd = filtrar(imagem, largura, altura, LIMITE)
salvar_pgm(ARQUIVO_SAIDA, largura, altura, maximo, filtrada)

print(f"Imagem {largura}x{altura} processada.")
print(f"Pixels corrigidos (ruído): {qtd}")
print(f"Resultado salvo em: {ARQUIVO_SAIDA}")
print(f"Limite: {LIMITE}")
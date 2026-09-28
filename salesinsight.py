# SalesInsight PY - Analise de Dados de Vendas
# Mini-Projeto do Modulo 01

import csv
import json
import os
import random
import re
from datetime import datetime, timedelta

# Meses
MESES = {1: "Janeiro", 2: "Fevereiro", 3: "Marco", 4: "Abril", 5: "Maio", 6: "Junho",
         7: "Julho", 8: "Agosto", 9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"}

# ---------- RF01 - gerar o dataset
def gerar_dataset_vendas(caminho_csv="vendas.csv", n_registros=200, seed=42):
    """Gera um dataset de vendas com alguns dados sujos e salva em CSV."""
    random.seed(seed)
    produtos = ["Notebook", "Smartphone", "Tablet", "Monitor", "Teclado", "Mouse", "Headset"]
    categorias = {"Notebook": "Computadores", "Smartphone": "Celulares", "Tablet": "Celulares",
                  "Monitor": "Computadores", "Teclado": "Perifericos", "Mouse": "Perifericos",
                  "Headset": "Perifericos"}
    precos = {"Notebook": 3500, "Smartphone": 2200, "Tablet": 1800, "Monitor": 1200,
              "Teclado": 250, "Mouse": 120, "Headset": 350}
    regioes = ["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"]
    data_inicio = datetime(2025, 1, 1)
    colunas = ["id_venda", "data_venda", "cliente", "produto",
               "categoria", "regiao", "quantidade", "preco_unitario"]

    with open(caminho_csv, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=colunas)
        escritor.writeheader()
        for i in range(n_registros):
            produto = random.choice(produtos)
            categoria = categorias[produto]
            quantidade = random.randint(1, 10)
            preco = round(precos[produto] * random.uniform(0.85, 1.15), 2)
            data = data_inicio + timedelta(days=random.randint(0, 364))
            data_txt = data.strftime("%Y-%m-%d")
            cliente = f"Cliente_{random.randint(1, 50):03d}"

            # sujeira proposital
            if random.random() < 0.05:
                quantidade = ""
            if random.random() < 0.04:
                preco = ""
            if random.random() < 0.06:
                produto = "  " + produto + "  "
            if random.random() < 0.03:
                data_txt = "DATA INVALIDA"
            if random.random() < 0.10:
                cliente = random.choice([cliente.upper().replace("_", "-"), cliente + "!!",
                                         "  " + cliente, cliente.replace("Cliente_", "cliente#")])

            escritor.writerow({"id_venda": i + 1, "data_venda": data_txt, "cliente": cliente,
                               "produto": produto, "categoria": categoria,
                               "regiao": random.choice(regioes), "quantidade": quantidade,
                               "preco_unitario": preco})
    print(f"Dataset gerado com {n_registros} registros.")

def carregar_dataset(caminho_csv):
    """Le o arquivo CSV e devolve uma lista de dicionarios."""
    with open(caminho_csv, "r", encoding="utf-8") as arquivo:
        registros = list(csv.DictReader(arquivo))
    return registros


def inspecionar_dados(registros):
    """Mostra quantos registros tem, as colunas, os vazios e as 5 primeiras linhas."""
    colunas = list(registros[0].keys())

    vazios = {}
    for coluna in colunas:
        vazios[coluna] = 0
    for linha in registros:
        for coluna in colunas:
            if linha[coluna].strip() == "":
                vazios[coluna] = vazios[coluna] + 1

    print("\n=== INSPECAO DOS DADOS ===")
    print("Total de registros:", len(registros))
    print("Colunas:", colunas)
    print("Valores vazios:", vazios)
    print("Primeiros registros:")
    for linha in registros[:5]:
        print(linha)

def limpar_dados(registros):
    """Remove registros com erro e padroniza os textos. Devolve a lista limpa e o relatorio."""
    relatorio = {"iniciais": len(registros), "removidos_data": 0, "removidos_vazios": 0,
                 "clientes_corrigidos": 0, "finais": 0}
    padrao_cliente = re.compile(r"^Cliente_\d{3}$")
    limpos = []

    for linha in registros:
        # tira espacos extras
        for chave in linha:
            linha[chave] = linha[chave].strip()

        # data: se nao converter, descarta
        try:
            linha["data_venda"] = datetime.strptime(linha["data_venda"], "%Y-%m-%d")
        except ValueError:
            relatorio["removidos_data"] += 1
            continue

        # quantidade ou preco vazio: descarta
        if linha["quantidade"] == "" or linha["preco_unitario"] == "":
            relatorio["removidos_vazios"] += 1
            continue

        # converte os numeros
        linha["quantidade"] = int(linha["quantidade"])
        linha["preco_unitario"] = float(linha["preco_unitario"])

        # cliente: marca se estava fora do padrao e corrige para Cliente_NNN
        linha["cliente_fora_do_padrao"] = padrao_cliente.match(linha["cliente"]) is None
        if linha["cliente_fora_do_padrao"]:
            relatorio["clientes_corrigidos"] += 1
        nome = re.sub(r"[^A-Za-z0-9_]", "", linha["cliente"])   # tira simbolos
        numero = re.search(r"\d+", nome).group()                # pega so o numero
        linha["cliente"] = "Cliente_" + numero.zfill(3)

        limpos.append(linha)

    relatorio["finais"] = len(limpos)
    print("\n=== RELATORIO DE LIMPEZA ===")
    print("Registros iniciais:", relatorio["iniciais"])
    print("Removidos por data invalida:", relatorio["removidos_data"])
    print("Removidos por valor vazio:", relatorio["removidos_vazios"])
    print("Registros finais:", relatorio["finais"])
    print("Nomes de cliente corrigidos:", relatorio["clientes_corrigidos"])
    return limpos, relatorio

# ---------- RF04 - colunas novas ----------
def criar_colunas_derivadas(registros):
    """Cria receita_total, mes, mes_nome, trimestre, ano e faixa_receita_item."""
    for linha in registros:
        data = linha["data_venda"]
        receita = linha["quantidade"] * linha["preco_unitario"]
        linha["receita_total"] = round(receita, 2)
        linha["mes"] = data.month
        linha["mes_nome"] = MESES[data.month]
        linha["ano"] = data.year

        if data.month <= 3:
            linha["trimestre"] = "Q1"
        elif data.month <= 6:
            linha["trimestre"] = "Q2"
        elif data.month <= 9:
            linha["trimestre"] = "Q3"
        else:
            linha["trimestre"] = "Q4"

        if receita < 500:
            linha["faixa_receita_item"] = "Baixo Valor"
        elif receita < 5000:
            linha["faixa_receita_item"] = "Medio Valor"
        else:
            linha["faixa_receita_item"] = "Alto Valor"
    return registros

# ---------- RF07 - funcao que recebe outra funcao ----------
def processar_coluna(registros, coluna, funcao, nome_saida):
    """Aplica a funcao recebida em uma coluna e guarda o resultado em nome_saida."""
    for linha in registros:
        linha[nome_saida] = funcao(linha[coluna])
    return registros


# ---------- RF05 - metricas ----------
def somar_por(registros, coluna):
    """Soma a receita agrupando pelos valores de uma coluna."""
    totais = {}
    for linha in registros:
        chave = linha[coluna]
        totais[chave] = totais.get(chave, 0) + linha["receita_total"]
    return totais


def calcular_metricas(registros):
    """Calcula as metricas por mes, trimestre, produto, categoria e regiao."""
    metricas = {}

    # por mes: receita, quantidade e numero de vendas
    por_mes = {}
    for linha in registros:
        mes = linha["mes"]
        if mes not in por_mes:
            por_mes[mes] = {"mes": mes, "mes_nome": MESES[mes], "receita_total": 0,
                            "quantidade": 0, "n_vendas": 0}
        por_mes[mes]["receita_total"] += linha["receita_total"]
        por_mes[mes]["quantidade"] += linha["quantidade"]
        por_mes[mes]["n_vendas"] += 1
    lista_mes = []
    for mes in sorted(por_mes):
        por_mes[mes]["receita_total"] = round(por_mes[mes]["receita_total"], 2)
        lista_mes.append(por_mes[mes])
    metricas["por_mes"] = lista_mes

    metricas["por_trimestre"] = somar_por(registros, "trimestre")

    # top 5 produtos (ordena do maior para o menor usando lambda)
    produtos = somar_por(registros, "produto")
    metricas["top_produtos"] = sorted(produtos.items(), key=lambda item: item[1], reverse=True)[:5]

    metricas["por_categoria"] = somar_por(registros, "categoria")

    # regiao: receita e ticket medio (receita / numero de vendas)
    receita_regiao = somar_por(registros, "regiao")
    vendas_regiao = {}
    for linha in registros:
        vendas_regiao[linha["regiao"]] = vendas_regiao.get(linha["regiao"], 0) + 1
    por_regiao = []
    for regiao in receita_regiao:
        ticket = receita_regiao[regiao] / vendas_regiao[regiao]
        por_regiao.append({"regiao": regiao, "receita_total": round(receita_regiao[regiao], 2),
                           "ticket_medio": round(ticket, 2)})
    metricas["por_regiao"] = por_regiao
    return metricas


def mostrar_metricas(metricas):
    """Imprime as metricas no console."""
    print("\n=== RECEITA POR MES ===")
    for m in metricas["por_mes"]:
        print(f"{m['mes_nome']:<10} R$ {m['receita_total']:>11.2f} | qtd {m['quantidade']:>3} | vendas {m['n_vendas']}")

    print("\n=== RECEITA POR TRIMESTRE ===")
    for tri in sorted(metricas["por_trimestre"]):
        print(f"{tri}  R$ {metricas['por_trimestre'][tri]:.2f}")

    print("\n=== TOP 5 PRODUTOS ===")
    for produto, receita in metricas["top_produtos"]:
        print(f"{produto:<11} R$ {receita:.2f}")

    print("\n=== RECEITA POR CATEGORIA ===")
    for categoria, receita in metricas["por_categoria"].items():
        print(f"{categoria:<13} R$ {receita:.2f}")

    print("\n=== RECEITA E TICKET MEDIO POR REGIAO ===")
    for r in metricas["por_regiao"]:
        print(f"{r['regiao']:<13} R$ {r['receita_total']:>11.2f} | ticket medio R$ {r['ticket_medio']:.2f}")

def segmentar_clientes(registros):
    """Soma o gasto de cada cliente e classifica em Bronze, Prata ou Ouro."""
    classificar = lambda total: "Ouro" if total > 15000 else "Prata" if total >= 5000 else "Bronze"

    gasto = somar_por(registros, "cliente")
    clientes = []
    for nome in gasto:
        clientes.append({"cliente": nome, "total_gasto": round(gasto[nome], 2),
                         "segmento": classificar(gasto[nome])})
    clientes.sort(key=lambda c: c["total_gasto"], reverse=True)

    print("\n=== TOP 10 CLIENTES ===")
    for c in clientes[:10]:
        print(f"{c['cliente']}  R$ {c['total_gasto']:.2f}  {c['segmento']}")

    contagem = {"Ouro": 0, "Prata": 0, "Bronze": 0}
    for c in clientes:
        contagem[c["segmento"]] += 1
    print("Clientes por segmento:", contagem)
    return clientes

def exportar_resultados(metricas, clientes, estatisticas):
    """Salva as metricas e os clientes em CSV, as estatisticas em JSON e le o JSON de volta."""
    os.makedirs("outputs", exist_ok=True)

    with open("outputs/metricas_por_mes.csv", "w", newline="", encoding="utf-8-sig") as f:
        escritor = csv.DictWriter(f, fieldnames=metricas["por_mes"][0].keys())
        escritor.writeheader()
        escritor.writerows(metricas["por_mes"])

    with open("outputs/segmentacao_clientes.csv", "w", newline="", encoding="utf-8-sig") as f:
        escritor = csv.DictWriter(f, fieldnames=clientes[0].keys())
        escritor.writeheader()
        escritor.writerows(clientes)

    with open("outputs/estatisticas_gerais.json", "w", encoding="utf-8") as f:
        json.dump(estatisticas, f, indent=4, ensure_ascii=False)

    with open("outputs/estatisticas_gerais.json", "r", encoding="utf-8") as f:
        conferencia = json.load(f)
    print("\n=== JSON LIDO DE VOLTA ===")
    print(conferencia)


def main():
    """Executa todas as etapas do projeto em ordem."""
    print("=" * 50)
    print("SALESINSIGHT PY - Analise de Dados de Vendas")
    print("=" * 50)

    if not os.path.exists("vendas.csv"):
        gerar_dataset_vendas("vendas.csv")

    registros = carregar_dataset("vendas.csv")
    inspecionar_dados(registros)

    registros, relatorio = limpar_dados(registros)       # limpeza vem antes de tudo
    registros = criar_colunas_derivadas(registros)

    # funcao que recebe outra funcao, usando lambda
    registros = processar_coluna(registros, "quantidade",
                                 lambda q: "Alto Volume" if q > 5 else "Baixo Volume",
                                 "perfil_volume")

    metricas = calcular_metricas(registros)
    mostrar_metricas(metricas)
    clientes = segmentar_clientes(registros)

    # estatisticas gerais
    receitas = [linha["receita_total"] for linha in registros]
    media = sum(receitas) / len(receitas)
    acima_da_media = 0
    for r in receitas:
        if r > media:
            acima_da_media += 1

    estatisticas = {"registros_iniciais": relatorio["iniciais"],
                    "registros_validos": relatorio["finais"],
                    "receita_total": round(sum(receitas), 2),
                    "ticket_medio": round(media, 2),
                    "vendas_acima_da_media": acima_da_media,
                    "total_clientes": len(clientes)}
    print("\n=== ESTATISTICAS GERAIS ===")
    print(estatisticas)

    exportar_resultados(metricas, clientes, estatisticas)
    print("\n[CONCLUIDO] Fluxo finalizado com sucesso.")


if __name__ == "__main__":
    main()
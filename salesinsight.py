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

def main():
    """Executa todas as etapas do projeto em ordem."""
    print("=" * 50)
    print("SALESINSIGHT PY - Analise de Dados de Vendas")
    print("=" * 50)

    if not os.path.exists("vendas.csv"):
        gerar_dataset_vendas("vendas.csv")


if __name__ == "__main__":
    main()
# SalesInsight PY

Mini-projeto do Módulo 01 — análise de dados de vendas em Python.

## Objetivo
Carregar, limpar e analisar um arquivo de vendas (`vendas.csv`) para responder:
- Como as vendas se comportam por mês e por trimestre?
- Quais produtos e categorias geram mais receita?
- Quais regiões vendem mais e qual o ticket médio de cada uma?
- Quais clientes são mais valiosos (Bronze, Prata ou Ouro)?
- Quantas vendas ficaram acima da média?

Os resultados são mostrados no terminal e salvos em CSV e JSON na pasta `outputs/`.

## Como executar
Precisa apenas do **Python 3.10 ou superior**. Não é necessário instalar nenhuma biblioteca.

**No computador (VS Code ou terminal):**
```bash
git clone https://github.com/rafhaelcinelli/salesinsight.git
cd salesinsight
python salesinsight.py
```

**No Google Colab:** faça upload do `salesinsight.py` e rode em uma célula:
```
!python salesinsight.py
```

Se o `vendas.csv` não existir, o próprio programa gera um novo (sempre igual, por causa do `seed=42`).

## Etapas do programa
| Etapa | Função |
|---|---|
| Gerar o dataset | `gerar_dataset_vendas()` |
| Carregar e inspecionar | `carregar_dataset()` e `inspecionar_dados()` |
| Limpar os dados | `limpar_dados()` |
| Criar colunas novas | `criar_colunas_derivadas()` |
| Aplicar uma função em uma coluna | `processar_coluna()` |
| Calcular e mostrar métricas | `somar_por()`, `calcular_metricas()` e `mostrar_metricas()` |
| Segmentar clientes | `segmentar_clientes()` |
| Exportar resultados | `exportar_resultados()` |
| Rodar tudo em ordem | `main()` |

## Conceitos aplicados
- Variáveis, tipos de dados e operadores
- `if / elif / else` (trimestre, faixa de receita e segmento)
- `for` para percorrer os registros
- Listas e dicionários
- Funções com parâmetros, retorno e docstring
- Funções `lambda` (segmentação, ordenação e `processar_coluna`)
- Função que recebe outra função (`processar_coluna`)
- Leitura e escrita de CSV (`csv.DictReader` e `csv.DictWriter`)
- Leitura e escrita de JSON (`json.dump` e `json.load`)
- Datas com `datetime` (`strptime`, `.month`, `.year`)
- Expressões regulares com `re` (`re.compile`, `re.sub`, `re.search`)
- Git e GitHub com branches e commits

## Resultado
- 200 registros lidos, 17 removidos (4 com data inválida e 13 com valor vazio), 183 válidos
- 15 nomes de cliente corrigidos
- Receita total: R$ 1.290.346,30 — ticket médio: R$ 7.051,07
- Melhor trimestre: Q4 — produto líder: Notebook — região líder: Nordeste
- Clientes: 34 Ouro, 10 Prata e 6 Bronze

## Decisão técnica
Registros com data inválida ou sem quantidade/preço são **removidos**, e não preenchidos, porque sem esses dados não dá para calcular a receita nem o mês da venda. Inventar valores deixaria as métricas erradas.

Os nomes de cliente são **corrigidos** com regex para o formato `Cliente_NNN`. Assim, `CLIENTE-016` e `cliente#016` viram o mesmo cliente e o gasto dele não fica dividido.

## O que pode melhorar
- Criar testes automáticos para a limpeza
- Permitir escolher o arquivo de entrada ao rodar o programa
- Adicionar gráficos

## Estrutura
```
salesinsight/
├── salesinsight.py
├── vendas.csv
├── README.md
├── outputs/
│   ├── metricas_por_mes.csv
│   ├── segmentacao_clientes.csv
│   └── estatisticas_gerais.json
└── planejamento/
    └── tarefas-kanban.md
```

## Vídeo de demonstração
[inserir aqui o link do vídeo]

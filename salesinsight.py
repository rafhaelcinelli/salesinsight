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
import pandas
from geobr import read_municipality


# Ler dados de cidades do Rio Grande do Sul
rs = read_municipality(code_muni="RS", year=2020)

# Processar os dados de vacinação do RS


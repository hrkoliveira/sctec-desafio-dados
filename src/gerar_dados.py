"""
Script para gerar dados simulados de empresas de Santa Catarina.
Os dados são baseados em distribuições realistas de setores, municípios e portes
empresariais do estado, simulando um cenário plausível de empreendedorismo.
"""

import csv
import random
import os
from datetime import datetime, timedelta

random.seed(42)

# Municípios de SC com pesos proporcionais à população/atividade econômica
MUNICIPIOS = {
    "Florianópolis": 0.12,
    "Joinville": 0.14,
    "Blumenau": 0.10,
    "Chapecó": 0.06,
    "Criciúma": 0.05,
    "Itajaí": 0.06,
    "Jaraguá do Sul": 0.04,
    "Lages": 0.03,
    "Balneário Camboriú": 0.05,
    "São José": 0.05,
    "Palhoça": 0.03,
    "Brusque": 0.03,
    "Tubarão": 0.02,
    "Navegantes": 0.02,
    "Concórdia": 0.02,
    "São Bento do Sul": 0.02,
    "Rio do Sul": 0.02,
    "Caçador": 0.015,
    "Gaspar": 0.015,
    "Indaial": 0.015,
    "Camboriú": 0.015,
    "Biguaçu": 0.01,
    "Araranguá": 0.01,
    "Canoinhas": 0.01,
    "Mafra": 0.01,
    "Xanxerê": 0.01,
    "Videira": 0.008,
    "Joaçaba": 0.008,
    "Imbituba": 0.007,
    "Laguna": 0.007,
}

# Mesorregiões de SC
MESORREGIAO = {
    "Florianópolis": "Grande Florianópolis",
    "São José": "Grande Florianópolis",
    "Palhoça": "Grande Florianópolis",
    "Biguaçu": "Grande Florianópolis",
    "Joinville": "Norte Catarinense",
    "Jaraguá do Sul": "Norte Catarinense",
    "São Bento do Sul": "Norte Catarinense",
    "Canoinhas": "Norte Catarinense",
    "Mafra": "Norte Catarinense",
    "Blumenau": "Vale do Itajaí",
    "Itajaí": "Vale do Itajaí",
    "Balneário Camboriú": "Vale do Itajaí",
    "Brusque": "Vale do Itajaí",
    "Navegantes": "Vale do Itajaí",
    "Gaspar": "Vale do Itajaí",
    "Indaial": "Vale do Itajaí",
    "Camboriú": "Vale do Itajaí",
    "Rio do Sul": "Vale do Itajaí",
    "Chapecó": "Oeste Catarinense",
    "Concórdia": "Oeste Catarinense",
    "Caçador": "Oeste Catarinense",
    "Xanxerê": "Oeste Catarinense",
    "Videira": "Oeste Catarinense",
    "Joaçaba": "Oeste Catarinense",
    "Criciúma": "Sul Catarinense",
    "Tubarão": "Sul Catarinense",
    "Araranguá": "Sul Catarinense",
    "Imbituba": "Sul Catarinense",
    "Laguna": "Sul Catarinense",
    "Lages": "Serrana",
}

# CNAEs simplificados com setores econômicos
SETORES = {
    "Comércio varejista": 0.22,
    "Alimentação e bebidas": 0.12,
    "Serviços profissionais": 0.10,
    "Construção civil": 0.08,
    "Tecnologia da informação": 0.09,
    "Saúde e bem-estar": 0.06,
    "Indústria têxtil e vestuário": 0.05,
    "Transporte e logística": 0.05,
    "Educação e treinamento": 0.04,
    "Agronegócio": 0.04,
    "Turismo e hotelaria": 0.03,
    "Imobiliário": 0.03,
    "Indústria metalúrgica": 0.03,
    "Indústria alimentícia": 0.03,
    "Beleza e estética": 0.03,
}

PORTES = {
    "MEI": 0.55,
    "ME": 0.25,
    "EPP": 0.12,
    "Média": 0.06,
    "Grande": 0.02,
}

NATUREZAS_JURIDICAS = {
    "MEI": "Empresário Individual",
    "ME": "Sociedade Limitada",
    "EPP": "Sociedade Limitada",
    "Média": "Sociedade Anônima Fechada",
    "Grande": "Sociedade Anônima",
}

# Faixas de capital social por porte (em R$)
CAPITAL_SOCIAL = {
    "MEI": (1000, 20000),
    "ME": (10000, 360000),
    "EPP": (360000, 4800000),
    "Média": (1000000, 50000000),
    "Grande": (10000000, 500000000),
}

# Faixa de funcionários por porte
FUNCIONARIOS = {
    "MEI": (0, 1),
    "ME": (1, 9),
    "EPP": (10, 49),
    "Média": (50, 249),
    "Grande": (250, 2000),
}

SITUACOES = ["Ativa", "Ativa", "Ativa", "Ativa", "Ativa", "Ativa", "Ativa",
             "Baixada", "Baixada", "Suspensa"]


def escolher_ponderado(opcoes: dict) -> str:
    itens = list(opcoes.keys())
    pesos = list(opcoes.values())
    return random.choices(itens, weights=pesos, k=1)[0]


def gerar_data_abertura(ano_inicio=2019, ano_fim=2025) -> str:
    inicio = datetime(ano_inicio, 1, 1)
    fim = datetime(ano_fim, 12, 31)
    delta = (fim - inicio).days
    data = inicio + timedelta(days=random.randint(0, delta))
    return data.strftime("%Y-%m-%d")


def gerar_cnpj_ficticio() -> str:
    numeros = [random.randint(0, 9) for _ in range(14)]
    return "{}{}.{}{}{}.{}{}{}/{}{}{}{}-{}{}".format(*numeros)


def gerar_empresa(id_empresa: int) -> dict:
    municipio = escolher_ponderado(MUNICIPIOS)
    setor = escolher_ponderado(SETORES)
    porte = escolher_ponderado(PORTES)
    situacao = random.choice(SITUACOES)
    data_abertura = gerar_data_abertura()

    capital_min, capital_max = CAPITAL_SOCIAL[porte]
    capital = round(random.uniform(capital_min, capital_max), 2)

    func_min, func_max = FUNCIONARIOS[porte]
    num_funcionarios = random.randint(func_min, func_max)

    data_situacao = ""
    if situacao == "Baixada":
        dt_abertura = datetime.strptime(data_abertura, "%Y-%m-%d")
        dias_ate_baixa = random.randint(90, 1500)
        dt_baixa = dt_abertura + timedelta(days=dias_ate_baixa)
        if dt_baixa > datetime(2025, 12, 31):
            situacao = "Ativa"
        else:
            data_situacao = dt_baixa.strftime("%Y-%m-%d")

    # Simular faturamento anual estimado (baseado no porte)
    faturamento_ranges = {
        "MEI": (12000, 81000),
        "ME": (81000, 360000),
        "EPP": (360000, 4800000),
        "Média": (4800000, 50000000),
        "Grande": (50000000, 500000000),
    }
    fat_min, fat_max = faturamento_ranges[porte]
    faturamento_anual = round(random.uniform(fat_min, fat_max), 2)

    # Introduzir valores ausentes/inconsistentes propositalmente (~5%)
    if random.random() < 0.03:
        num_funcionarios = None
    if random.random() < 0.02:
        capital = None
    if random.random() < 0.02:
        faturamento_anual = -1  # valor inconsistente
    if random.random() < 0.01:
        municipio = ""  # valor ausente

    return {
        "id": id_empresa,
        "cnpj": gerar_cnpj_ficticio(),
        "municipio": municipio,
        "mesorregiao": MESORREGIAO.get(municipio, "Não informada"),
        "setor": setor,
        "porte": porte,
        "natureza_juridica": NATUREZAS_JURIDICAS[porte],
        "capital_social": capital,
        "num_funcionarios": num_funcionarios,
        "faturamento_anual_estimado": faturamento_anual,
        "data_abertura": data_abertura,
        "situacao": situacao,
        "data_situacao": data_situacao,
    }


def main():
    num_empresas = 5000
    empresas = [gerar_empresa(i + 1) for i in range(num_empresas)]

    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, "empresas_sc.csv")

    campos = [
        "id", "cnpj", "municipio", "mesorregiao", "setor", "porte",
        "natureza_juridica", "capital_social", "num_funcionarios",
        "faturamento_anual_estimado", "data_abertura", "situacao", "data_situacao",
    ]

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(empresas)

    print(f"Dados gerados: {len(empresas)} empresas em {filepath}")


if __name__ == "__main__":
    main()

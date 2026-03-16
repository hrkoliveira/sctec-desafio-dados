# Análise Exploratória do Empreendedorismo em Santa Catarina

## Descrição

Este projeto realiza uma **Análise Exploratória de Dados (AED)** sobre o cenário empreendedor do estado de Santa Catarina, investigando padrões de abertura e fechamento de empresas, distribuição por setores econômicos, portes empresariais e regiões do estado.

A análise abrange um dataset de **5.000 empresas** e gera visualizações que permitem compreender a dinâmica do empreendedorismo catarinense, incluindo concentração geográfica, sazonalidade de aberturas, taxa de mortalidade por setor e correlações entre variáveis financeiras.

## Origem do Conjunto de Dados

O conjunto de dados foi **simulado programaticamente** (`src/gerar_dados.py`) com distribuições proporcionais baseadas em dados reais de atividade econômica de Santa Catarina. Os pesos de municípios, setores e portes foram calibrados para refletir a realidade econômica do estado, considerando:

- **Municípios**: pesos proporcionais à população e atividade econômica (Joinville, Florianópolis e Blumenau como maiores polos)
- **Setores**: distribuição inspirada nos CNAEs mais frequentes em SC (comércio varejista, alimentação, TI, indústria têxtil)
- **Portes**: distribuição realista com predominância de MEI (55%) e ME (25%)
- **Mesorregiões**: mapeamento correto dos municípios nas 6 mesorregiões de SC

Os dados incluem propositalmente ~5% de valores ausentes e inconsistentes para demonstrar técnicas de tratamento.

## Etapas Realizadas

### 1. Geração e Carregamento dos Dados
Script Python que gera 5.000 registros com 13 variáveis cada, incluindo CNPJ fictício, município, setor, porte, capital social, número de funcionários, faturamento estimado e situação cadastral.

### 2. Tratamento de Dados
- Identificação e contagem de valores nulos por coluna
- Detecção de strings vazias em campos categóricos
- Correção de faturamentos negativos (valores inconsistentes)
- Preenchimento de valores ausentes com mediana estratificada por porte
- Conversão de tipos de dados (datas, inteiros)

### 3. Análise Estatística Descritiva
- Estatísticas descritivas das variáveis numéricas (média, mediana, desvio padrão)
- Distribuição por situação cadastral e cálculo da taxa de mortalidade

### 4. Visualizações Geradas
| Gráfico | Descrição |
|---------|-----------|
| Setores Econômicos | Barras horizontais + pizza dos 5 principais setores |
| Porte Empresarial | Distribuição de empresas e faturamento médio por porte |
| Distribuição Geográfica | Top 15 municípios + pizza por mesorregião |
| Análise Temporal | Aberturas por ano + sazonalidade mensal |
| Mortalidade por Setor | Taxa de mortalidade com destaque acima/abaixo da média |
| Capital vs Faturamento | Scatter plot com escala log + boxplot de funcionários |
| Heatmap Setor x Região | Concentração de empresas por setor e mesorregião |
| Evolução dos Setores | Linha temporal dos 5 principais setores (2019-2025) |

### 5. Conclusões
- MEI e ME representam mais de 80% das empresas
- Vale do Itajaí e Norte concentram a maior atividade empresarial
- Comércio varejista é o setor dominante
- TI mostra crescimento consistente, especialmente em Florianópolis

## Tecnologias Empregadas

- **Python 3.12** — linguagem principal
- **pandas 3.0** — manipulação e análise de dados
- **matplotlib 3.10** — visualizações estáticas
- **seaborn 0.13** — visualizações estatísticas
- **Jupyter Notebook** — ambiente interativo de desenvolvimento

## Estrutura do Projeto

```
sctec-desafio-dados/
├── README.md                  # Documentação do projeto
├── requirements.txt           # Dependências Python
├── .gitignore                 # Arquivos ignorados pelo Git
├── data/
│   └── empresas_sc.csv        # Dataset (5.000 registros)
├── notebooks/
│   └── analise_exploratoria.ipynb  # Notebook principal da análise
├── src/
│   ├── gerar_dados.py         # Script de geração do dataset
│   ├── analise.py             # Script standalone (alternativa ao notebook)
│   └── criar_notebook.py      # Script auxiliar de criação do notebook
└── outputs/
    ├── setores_economicos.png
    ├── porte_empresarial.png
    ├── distribuicao_geografica.png
    ├── analise_temporal.png
    ├── mortalidade_setor.png
    ├── capital_funcionarios.png
    ├── heatmap_setor_regiao.png
    └── evolucao_setores.png
```

## Instruções para Execução

### Pré-requisitos
- Python 3.10 ou superior
- pip (gerenciador de pacotes)

### Instalação

```bash
# Clonar o repositório
git clone https://github.com/hrkoliveira/sctec-desafio-dados.git
cd sctec-desafio-dados

# Criar e ativar ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt
```

### Executar

**Opção 1 — Jupyter Notebook (recomendado):**
```bash
# Abrir o notebook interativo
jupyter notebook notebooks/analise_exploratoria.ipynb
```
O notebook pode ser executado célula a célula ou de uma vez com `Cell > Run All`.

**Opção 2 — Script standalone (sem Jupyter):**
```bash
# Executar análise completa via terminal
python src/analise.py
```
Imprime estatísticas no terminal e salva os gráficos em `outputs/`.

**Gerar dados novamente (opcional):**
```bash
python src/gerar_dados.py
```
O CSV já está incluso no repositório — só necessário se quiser regenerar.

## Vídeo Pitch

[Assistir o vídeo pitch no YouTube](https://youtu.be/dVJOA_o3zpQ)

---

**Desafio SCTEC — IA para Devs**
Candidato: Herik Oliveira

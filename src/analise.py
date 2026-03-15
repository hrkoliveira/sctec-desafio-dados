"""
Script standalone de análise exploratória.
Alternativa ao notebook Jupyter — executa toda a análise e salva os gráficos.
"""

import os
import sys

import matplotlib
matplotlib.use('Agg')  # Backend não-interativo

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Configurações globais
sns.set_theme(style='whitegrid', palette='Set2')
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['figure.dpi'] = 100
plt.rcParams['font.size'] = 11

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'empresas_sc.csv')
OUTPUT_DIR = os.path.join(BASE_DIR, 'outputs')


def carregar_dados() -> pd.DataFrame:
    """Carrega o dataset de empresas."""
    print("=" * 60)
    print("ANÁLISE EXPLORATÓRIA — EMPREENDEDORISMO EM SC")
    print("=" * 60)

    df = pd.read_csv(DATA_PATH)
    print(f"\nDataset carregado: {df.shape[0]:,} registros, {df.shape[1]} colunas")
    return df


def tratar_dados(df: pd.DataFrame) -> pd.DataFrame:
    """Trata valores ausentes e inconsistentes."""
    print("\n--- TRATAMENTO DE DADOS ---")

    # Valores ausentes
    ausentes = df.isnull().sum()
    total_ausentes = ausentes.sum()
    print(f"Valores ausentes encontrados: {total_ausentes}")

    # Strings vazias
    vazios_mun = (df['municipio'] == '').sum()
    if vazios_mun > 0:
        print(f"Municípios vazios: {vazios_mun}")

    # Faturamento negativo
    negativos = (df['faturamento_anual_estimado'] < 0).sum()
    if negativos > 0:
        print(f"Faturamentos negativos: {negativos}")

    # Aplicar tratamentos
    df['municipio'] = df['municipio'].replace('', 'Não informado')
    df.loc[df['municipio'] == 'Não informado', 'mesorregiao'] = 'Não informada'

    for porte in df['porte'].unique():
        mask_func = (df['porte'] == porte) & (df['num_funcionarios'].isnull())
        if mask_func.any():
            mediana = df.loc[df['porte'] == porte, 'num_funcionarios'].median()
            df.loc[mask_func, 'num_funcionarios'] = mediana

        mask_cap = (df['porte'] == porte) & (df['capital_social'].isnull())
        if mask_cap.any():
            mediana = df.loc[df['porte'] == porte, 'capital_social'].median()
            df.loc[mask_cap, 'capital_social'] = mediana

        mask_fat = (df['porte'] == porte) & (df['faturamento_anual_estimado'] < 0)
        if mask_fat.any():
            mediana = df.loc[
                (df['porte'] == porte) & (df['faturamento_anual_estimado'] > 0),
                'faturamento_anual_estimado'
            ].median()
            df.loc[mask_fat, 'faturamento_anual_estimado'] = mediana

    df['num_funcionarios'] = df['num_funcionarios'].astype(int)
    df['data_abertura'] = pd.to_datetime(df['data_abertura'])
    df['ano_abertura'] = df['data_abertura'].dt.year
    df['mes_abertura'] = df['data_abertura'].dt.month

    print("Tratamento concluído!")
    return df


def analise_descritiva(df: pd.DataFrame) -> None:
    """Imprime estatísticas descritivas."""
    print("\n--- ANÁLISE DESCRITIVA ---")

    print(f"\nTotal de empresas: {len(df):,}")

    situacao = df['situacao'].value_counts()
    for sit, count in situacao.items():
        pct = count / len(df) * 100
        print(f"  {sit}: {count:,} ({pct:.1f}%)")

    baixadas = situacao.get('Baixada', 0)
    print(f"\nTaxa de mortalidade: {baixadas / len(df) * 100:.1f}%")

    print("\nTop 5 setores:")
    for setor, count in df['setor'].value_counts().head(5).items():
        print(f"  {setor}: {count:,}")

    print("\nTop 5 municípios:")
    mun = df[df['municipio'] != 'Não informado']['municipio'].value_counts().head(5)
    for m, count in mun.items():
        print(f"  {m}: {count:,}")

    print("\nPor porte:")
    for porte, count in df['porte'].value_counts().items():
        fat_medio = df.loc[df['porte'] == porte, 'faturamento_anual_estimado'].mean()
        print(f"  {porte}: {count:,} empresas | faturamento médio: R$ {fat_medio:,.2f}")


def gerar_graficos(df: pd.DataFrame) -> None:
    """Gera e salva todos os gráficos."""
    print("\n--- GERANDO GRÁFICOS ---")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 1. Setores
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    setor_counts = df['setor'].value_counts()
    setor_counts.plot(kind='barh', ax=axes[0], color=sns.color_palette('Set2', len(setor_counts)))
    axes[0].set_title('Empresas por Setor Econômico', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Quantidade')
    axes[0].set_ylabel('')
    top5 = setor_counts.head(5)
    outros = pd.Series({'Outros': setor_counts.tail(len(setor_counts) - 5).sum()})
    pd.concat([top5, outros]).plot(kind='pie', ax=axes[1], autopct='%1.1f%%', startangle=90,
                                   colors=sns.color_palette('Set2', 6))
    axes[1].set_title('Top 5 Setores', fontsize=14, fontweight='bold')
    axes[1].set_ylabel('')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'setores_economicos.png'), bbox_inches='tight', dpi=150)
    plt.close()
    print("  [OK] setores_economicos.png")

    # 2. Portes
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    ordem = ['MEI', 'ME', 'EPP', 'Média', 'Grande']
    cores = ['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3', '#a6d854']
    df['porte'].value_counts().reindex(ordem).plot(kind='bar', ax=axes[0], color=cores)
    axes[0].set_title('Distribuição por Porte', fontsize=14, fontweight='bold')
    axes[0].tick_params(axis='x', rotation=0)
    df.groupby('porte')['faturamento_anual_estimado'].mean().reindex(ordem).plot(
        kind='bar', ax=axes[1], color=cores)
    axes[1].set_title('Faturamento Médio por Porte', fontsize=14, fontweight='bold')
    axes[1].set_yscale('log')
    axes[1].tick_params(axis='x', rotation=0)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'porte_empresarial.png'), bbox_inches='tight', dpi=150)
    plt.close()
    print("  [OK] porte_empresarial.png")

    # 3. Geografia
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    mun = df[df['municipio'] != 'Não informado']['municipio'].value_counts().head(15)
    mun.plot(kind='barh', ax=axes[0], color=sns.color_palette('viridis', 15))
    axes[0].set_title('Top 15 Municípios', fontsize=14, fontweight='bold')
    axes[0].invert_yaxis()
    meso = df[df['mesorregiao'] != 'Não informada']['mesorregiao'].value_counts()
    meso.plot(kind='pie', ax=axes[1], autopct='%1.1f%%', colors=sns.color_palette('Set3', len(meso)))
    axes[1].set_title('Por Mesorregião', fontsize=14, fontweight='bold')
    axes[1].set_ylabel('')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'distribuicao_geografica.png'), bbox_inches='tight', dpi=150)
    plt.close()
    print("  [OK] distribuicao_geografica.png")

    # 4. Temporal
    fig, axes = plt.subplots(2, 1, figsize=(14, 10))
    abertura_ano = df.groupby('ano_abertura').size()
    abertura_ano.plot(kind='bar', ax=axes[0], color='#66c2a5')
    axes[0].set_title('Empresas Abertas por Ano', fontsize=14, fontweight='bold')
    axes[0].tick_params(axis='x', rotation=0)
    abertura_mes = df.groupby('mes_abertura').size()
    meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    abertura_mes.index = meses
    abertura_mes.plot(kind='line', ax=axes[1], marker='o', linewidth=2.5, color='#fc8d62')
    axes[1].fill_between(range(12), abertura_mes.values, alpha=0.2, color='#fc8d62')
    axes[1].set_title('Sazonalidade (2019-2025)', fontsize=14, fontweight='bold')
    axes[1].set_xticks(range(12))
    axes[1].set_xticklabels(meses)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'analise_temporal.png'), bbox_inches='tight', dpi=150)
    plt.close()
    print("  [OK] analise_temporal.png")

    # 5. Mortalidade
    mortalidade = df.groupby('setor').apply(
        lambda x: (x['situacao'] == 'Baixada').sum() / len(x) * 100
    ).sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(14, 7))
    colors_mort = ['#e74c3c' if v > mortalidade.mean() else '#2ecc71' for v in mortalidade.values]
    mortalidade.plot(kind='barh', ax=ax, color=colors_mort)
    ax.axvline(mortalidade.mean(), color='#333', linestyle='--', label=f'Média: {mortalidade.mean():.1f}%')
    ax.set_title('Taxa de Mortalidade por Setor', fontsize=14, fontweight='bold')
    ax.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'mortalidade_setor.png'), bbox_inches='tight', dpi=150)
    plt.close()
    print("  [OK] mortalidade_setor.png")

    # 6. Capital x Funcionários
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    sample = df[df['porte'].isin(['ME', 'EPP', 'Média'])].sample(500, random_state=42)
    axes[0].scatter(sample['capital_social'], sample['faturamento_anual_estimado'],
                    c=sample['porte'].map({'ME': 0, 'EPP': 1, 'Média': 2}), cmap='Set2', alpha=0.6, s=30)
    axes[0].set_xscale('log')
    axes[0].set_yscale('log')
    axes[0].set_title('Capital vs Faturamento', fontsize=13, fontweight='bold')
    sns.boxplot(data=df, x='porte', y='num_funcionarios', order=ordem, ax=axes[1], palette='Set2')
    axes[1].set_title('Funcionários por Porte', fontsize=13, fontweight='bold')
    axes[1].set_yscale('log')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'capital_funcionarios.png'), bbox_inches='tight', dpi=150)
    plt.close()
    print("  [OK] capital_funcionarios.png")

    # 7. Heatmap
    cross = pd.crosstab(df['setor'], df['mesorregiao'])
    cross = cross.drop(columns=['Não informada'], errors='ignore')
    fig, ax = plt.subplots(figsize=(14, 10))
    sns.heatmap(cross, annot=True, fmt='d', cmap='YlOrRd', ax=ax, linewidths=0.5)
    ax.set_title('Setor x Mesorregião', fontsize=14, fontweight='bold')
    plt.xticks(rotation=30, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'heatmap_setor_regiao.png'), bbox_inches='tight', dpi=150)
    plt.close()
    print("  [OK] heatmap_setor_regiao.png")

    # 8. Evolução setores
    top5_set = df['setor'].value_counts().head(5).index.tolist()
    evolucao = df[df['setor'].isin(top5_set)].groupby(['ano_abertura', 'setor']).size().unstack(fill_value=0)
    fig, ax = plt.subplots(figsize=(14, 7))
    evolucao.plot(kind='line', ax=ax, marker='o', linewidth=2)
    ax.set_title('Evolução dos 5 Principais Setores', fontsize=14, fontweight='bold')
    ax.legend(title='Setor', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'evolucao_setores.png'), bbox_inches='tight', dpi=150)
    plt.close()
    print("  [OK] evolucao_setores.png")

    print(f"\nTodos os gráficos salvos em: {OUTPUT_DIR}")


def main():
    df = carregar_dados()
    df = tratar_dados(df)
    analise_descritiva(df)
    gerar_graficos(df)
    print("\n" + "=" * 60)
    print("Análise concluída com sucesso!")
    print("=" * 60)


if __name__ == "__main__":
    main()

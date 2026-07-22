import pandas as pd


def obter_ranking_recente(nome_jogador, df):
    """Devolve o ranking mais recente de um jogador, procurando nas colunas
    Player_1 e Player_2. Devolve None se o jogador não existir nos dados."""
    jogos_como_p1 = df[df['Player_1'] == nome_jogador][['Date', 'Rank_1']].rename(columns={'Rank_1': 'Rank'})
    jogos_como_p2 = df[df['Player_2'] == nome_jogador][['Date', 'Rank_2']].rename(columns={'Rank_2': 'Rank'})

    todos_jogos = pd.concat([jogos_como_p1, jogos_como_p2])

    if len(todos_jogos) == 0:
        return None

    todos_jogos = todos_jogos.sort_values('Date', ascending=False)
    return todos_jogos.iloc[0]['Rank']


def prever_jogo(jogador1, jogador2, superficie, modelo, df):
    """Prevê o resultado de um jogo entre dois jogadores, dado o modelo treinado
    e o DataFrame com o histórico de jogos (para obter os rankings mais recentes)."""
    rank1 = obter_ranking_recente(jogador1, df)
    rank2 = obter_ranking_recente(jogador2, df)

    if rank1 is None:
        print(f"Jogador '{jogador1}' não encontrado nos dados.")
        return None
    if rank2 is None:
        print(f"Jogador '{jogador2}' não encontrado nos dados.")
        return None

    surface_clay = 1 if superficie == 'Clay' else 0
    surface_grass = 1 if superficie == 'Grass' else 0
    surface_hard = 1 if superficie == 'Hard' else 0

    dados_jogo = pd.DataFrame({
        'Rank_1': [rank1],
        'Rank_2': [rank2],
        'Surface_Clay': [surface_clay],
        'Surface_Grass': [surface_grass],
        'Surface_Hard': [surface_hard]
    })

    probabilidades = modelo.predict_proba(dados_jogo)[0]
    prob_jogador1 = probabilidades[1]

    print(f"{jogador1} (rank {int(rank1)}) vs {jogador2} (rank {int(rank2)}) em {superficie}")
    print(f"Probabilidade de {jogador1} vencer: {prob_jogador1:.1%}")
    print(f"Probabilidade de {jogador2} vencer: {1 - prob_jogador1:.1%}")

    return prob_jogador1
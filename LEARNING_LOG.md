# Learning Log — Tennis Predictor

## 20/07/2026

### O que fiz
- Instalei o Git no Windows
- Configurei a identidade do Git (`user.name` e `user.email`)
- Criei a estrutura do projeto: pastas `data/`, `notebooks/`, `src/`
- Criei e preenchi `.gitignore`, `requirements.txt`, `README.md`
- Criei um ambiente virtual (venv) dedicado ao projeto
- Instalei as bibliotecas: pandas, scikit-learn, jupyter, matplotlib
- Inicializei o repositório Git local e fiz o primeiro commit
- Criei o repositório no GitHub e fiz push do código

### Comandos novos que aprendi

**Git:**
- `git init` — inicializa um repositório Git na pasta atual
- `git config --global user.name "..."` / `user.email "..."` — configura a identidade para os commits (feito uma vez por computador)
- `git add .` — prepara todos os ficheiros (exceto os do `.gitignore`) para o próximo commit
- `git commit -m "mensagem"` — grava uma "fotografia" do estado atual do projeto, com uma mensagem descritiva
- `git remote add origin <url>` — liga o repositório local a um repositório remoto (no GitHub), com o apelido "origin"
- `git branch -M main` — renomeia a branch atual para "main"
- `git push -u origin main` — envia os commits locais para o GitHub; o `-u` faz o Git lembrar-se desta ligação para próximos pushes

**Terminal (Windows):**
- `cd <pasta>` — muda de pasta
- `mkdir <nome>` — cria uma pasta nova
- `type nul > <ficheiro>` — cria um ficheiro vazio
- `dir` — lista o conteúdo da pasta atual

**Python:**
- `python -m venv venv` — cria um ambiente virtual chamado "venv" na pasta atual
- `venv\Scripts\activate` — ativa o ambiente virtual (Windows)
- `deactivate` — desativa o ambiente virtual ativo
- `pip install -r requirements.txt` — instala todas as bibliotecas listadas no ficheiro

### Conceitos-chave
- **Git vs GitHub:** Git é o sistema de controlo de versões local; GitHub é o serviço na cloud onde guardo/partilho os repositórios
- **venv:** ambiente isolado por projeto, para não misturar bibliotecas entre projetos diferentes
- **.gitignore:** lista de ficheiros/pastas que o Git deve ignorar (ex: venv/, cache)
- **requirements.txt:** lista de dependências do projeto, para instalação reprodutível noutra máquina

### Próximos passos
- Carregar o dataset de ténis (Jeff Sackmann - ATP results)
- Explorar os dados num notebook Jupyter
- Começar a pensar em feature engineering (ex: diferença de ranking, desempenho por superfície)


## 22/07/2026

### O que fiz
- Descarreguei o dataset ATP Tennis (2000-2026) do Kaggle, guardado em `data/atp_tennis.csv` (o repositório original do Jeff Sackmann no GitHub deixou de estar acessível)
- Criei o notebook `01_exploracao.ipynb` e liguei-o ao venv do projeto
- Explorei os dados: 68.300 jogos, 17 colunas, sem valores nulos "oficiais"
- Descobri que várias colunas (Rank, Pts, Odds) usam `-1` como código para "dado desconhecido" — não são valores reais
- Limpei as ~14 linhas com Rank_1/Rank_2 inválidos (mantive Pts e Odds de fora do modelo por agora, por terem 23% e 5.5% de dados em falta respetivamente)
- Criei a variável target `Player_1_Won` (0 ou 1) a partir da coluna `Winner`
- Fiz one-hot encoding da coluna `Surface` (Hard, Clay, Grass, Carpet)
- Separei os dados em treino (80%, 54.619 jogos) e teste (20%, 13.655 jogos)
- Treinei o primeiro modelo: Regressão Logística, usando Rank_1, Rank_2 e Surface como features
- Resultado: **65.40% de accuracy** no conjunto de teste

### Comandos/conceitos novos que aprendi

**Pandas:**
- `df.head()` / `df.tail()` — mostra as primeiras/últimas N linhas
- `df.info()` — resumo de colunas, tipos de dados e valores não-nulos
- `df.describe()` — estatísticas (média, min, max, quartis) das colunas numéricas
- `df['coluna'].value_counts()` — conta ocorrências de cada valor único numa coluna
- Filtragem condicional: `df[(condição1) & (condição2)]`
- `.copy()` — evita o aviso SettingWithCopyWarning ao criar um DataFrame derivado
- `pd.get_dummies()` — one-hot encoding de colunas categóricas
- `pd.concat([...], axis=1)` — junta DataFrames lado a lado (por colunas)

**Scikit-learn:**
- `train_test_split()` — separa dados em treino/teste (`test_size`, `random_state` para reprodutibilidade)
- `LogisticRegression()` — modelo de classificação binária
- `.fit(X_train, y_train)` — treina o modelo
- `.predict(X_test)` — gera previsões
- `accuracy_score(y_test, y_pred)` — mede a percentagem de acertos

### Conceitos-chave
- **Feature vs. Target:** features (X) são os inputs; target (y) é o que queremos prever
- **One-hot encoding:** necessário para variáveis categóricas sem ordem natural, para não sugerir uma hierarquia falsa ao modelo
- **Treino vs. Teste:** nunca avaliar um modelo com os mesmos dados usados para o treinar
- **Accuracy como baseline:** no ténis, ~65-68% é o patamar esperado só com base no ranking; acima de 75-80% seria motivo de desconfiança

### Próximos passos (ideias para continuar)
1. Analisar *onde* o modelo erra mais (ex: jogos com rankings próximos/equilibrados)
2. Criar a feature `Rank_Diff` (diferença de ranking entre os dois jogadores) — pode ser mais informativa que os rankings absolutos
3. Experimentar outro algoritmo (ex: Random Forest) e comparar accuracy
4. Reintroduzir `Pts_1`/`Pts_2` e `Odd_1`/`Odd_2` com tratamento adequado dos valores em falta, e comparar se melhora o modelo

## 23/07/2026

### O que fiz
- Criei a feature `Rank_Diff` (diferença de ranking entre os dois jogadores) e testei-a tanto na Regressão Logística como no Random Forest — em ambos os casos, não trouxe melhoria (informação redundante face a Rank_1/Rank_2)
- Treinei um Random Forest e comparei com a Regressão Logística baseline
- Detetei overfitting no Random Forest por defeito (87.50% treino vs 58.95% teste) e corrigi limitando a profundidade das árvores (`max_depth=5`), resultando em 65.52% treino vs 65.23% teste — já sem overfitting, e praticamente equivalente à Regressão Logística (65.40%)
- Construí a função `obter_ranking_recente()`, que procura o ranking mais atual de um jogador no dataset (procurando tanto em Player_1 como em Player_2)
- Construí a função `prever_jogo()`, que recebe dois nomes de jogadores + superfície, e devolve a probabilidade de vitória de cada um, usando o modelo treinado
- Testei com jogadores reais (ex: Tsitsipas vs Rublev em Hard) — resultado coerente com o ranking
- Movi as duas funções para `src/predict.py`, e passei a importá-las no notebook via `sys.path.append()` + `from predict import ...`, em vez de as ter duplicadas

### Comandos/conceitos novos que aprendi

**Scikit-learn:**
- `RandomForestClassifier()` — modelo baseado em múltiplas árvores de decisão, combinando "votos"
- `max_depth` — parâmetro que limita a complexidade das árvores, para evitar overfitting
- `.predict_proba()` — devolve as probabilidades de cada classe (em vez de só 0/1 como o `.predict()`), formato `[[prob_classe_0, prob_classe_1]]`

**Pandas:**
- `.iloc[posição]` vs `.loc[índice]` — `.iloc` acede pela posição física da linha (útil depois de `sort_values`, quando os índices originais ficam "desordenados"); `.loc` acede pelo rótulo/índice
- `pd.concat([...])` sem `axis=1` — junta DataFrames por linhas (empilha), ao contrário do `axis=1` que junta por colunas

**Organização de projeto:**
- `sys.path.append('../pasta')` — permite importar módulos de outras pastas do projeto
- `from ficheiro import funcao1, funcao2` — importa funções específicas de um ficheiro `.py` próprio
- Docstrings (`"""texto"""` a seguir a um `def`) — forma padrão de documentar funções em Python

### Conceitos-chave
- **Overfitting:** quando um modelo "decora" os dados de treino em vez de aprender um padrão geral — sinal claro é accuracy muito mais alta no treino do que no teste
- **Multicolinearidade:** quando uma feature é calculada diretamente a partir de outras já existentes (ex: Rank_Diff a partir de Rank_1/Rank_2), raramente acrescenta informação nova ao modelo
- **Modelo mais complexo ≠ modelo melhor:** com poucas features simples, um Random Forest bem afinado tende a convergir para resultados semelhantes a um modelo linear simples
- **Notebook vs. src/:** notebook para experimentação; src/ para código já validado e reutilizável

### Próximos passos (ideias para continuar)
1. Explorar mais casos de teste na função `prever_jogo()` (jogadores conhecidos, diferentes superfícies)
2. Reintroduzir `Pts_1`/`Pts_2` e `Odd_1`/`Odd_2` com tratamento adequado dos valores em falta, e ver se melhora o modelo
3. Considerar ligar a uma fonte de ranking atualizada (API) em vez de depender só do ranking mais recente presente no dataset histórico
4. Continuar a mover código estável do notebook para `src/` à medida que se consolida
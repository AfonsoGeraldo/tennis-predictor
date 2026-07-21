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
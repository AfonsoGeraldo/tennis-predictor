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
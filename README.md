# From Scratch

Aplicacao web de tarefas criada para aprendizado. O projeto demonstra um fluxo completo entre:

- **Frontend:** React 19 + Vite
- **Backend:** FastAPI + Uvicorn
- **Banco de dados:** MongoDB

O sistema permite criar, listar, atualizar, concluir e excluir tarefas. A API tambem possui endpoints de health check. A versao atual e um MVP local, sem autenticacao.

## Repositorios

Este repositorio contem o codigo executavel da aplicacao. A documentacao de planejamento e arquitetura fica em um repositorio separado, chamado `project-map`, quando os dois projetos estao lado a lado no computador.

## Pre-requisitos

Instale antes de iniciar:

- Git
- Python 3.10 ou superior
- Node.js e npm
- MongoDB local, em execucao na porta `27017`

Confira as instalacoes:

```bash
git --version
python --version
node --version
npm --version
```

## Copiar o projeto

Para obter uma copia a partir do GitHub, substitua `SEU_USUARIO` pelo dono do repositorio:

```bash
cd /c/Projetos
git clone https://github.com/SEU_USUARIO/from-scratch.git
cd from-scratch
```

Se voce recebeu os arquivos por outro meio, basta abrir a pasta `from-scratch` no VS Code. Para atualizar uma copia que ja foi clonada:

```bash
git pull origin main
```

## Configurar e executar o backend

No Git Bash, abra um terminal na raiz do projeto e execute:

```bash
cd /c/Projetos/from-scratch/backend
python -m venv .venv
source .venv/Scripts/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

O backend ficara disponivel em `http://localhost:8000`. A documentacao interativa da API esta em `http://localhost:8000/docs`.

> O MongoDB precisa estar iniciado antes de executar o backend. Por padrao, a aplicacao usa `mongodb://localhost:27017`, o banco `tasks_db` e a colecao `tasks`.

## Configurar e executar o frontend

Mantenha o backend executando e abra um segundo terminal do Git Bash:

```bash
cd /c/Projetos/from-scratch/frontend
npm install
npm run dev
```

Abra o endereco mostrado pelo Vite, normalmente `http://localhost:5173`.

Comandos uteis do frontend:

```bash
npm run build    # gera a versao de producao
npm run lint     # verifica problemas de lint
npm run preview  # testa a versao de producao localmente
```

## Estrutura principal

```text
from-scratch/
├── backend/
│   ├── database.py       # conexao com MongoDB
│   ├── main.py           # rotas da API FastAPI
│   ├── models.py         # modelos e validacoes Pydantic
│   └── requirements.txt  # dependencias Python
├── frontend/
│   ├── src/App.jsx       # interface principal
│   ├── src/api.js        # chamadas para a API
│   └── package.json      # scripts e dependencias JavaScript
├── docs/                 # guias auxiliares
└── .specs/               # especificacoes da feature de autenticacao
```

## Fluxo basico com Git

Crie uma branch para cada tarefa, faca commits pequenos e abra um Pull Request para `main`:

```bash
git switch main
git pull origin main
git switch -c feat/auth-T1

# faca as alteracoes
git add .
git commit -m "feat: implementar base da autenticacao"
git push -u origin feat/auth-T1
```

Depois, no GitHub, escolha **Compare & pull request**, usando `main` como branch de destino.

## Limites atuais

- A autenticacao ainda nao foi implementada.
- O endpoint `DELETE /api/tasks` apaga todas as tarefas e deve ser usado apenas em desenvolvimento.
- O backend depende de um MongoDB local.

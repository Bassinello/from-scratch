# Frontend

Interface web do projeto de tarefas. Este pacote usa React 19, Vite e Axios para consumir a API FastAPI do diretorio [`backend`](../backend/).

## Pre-requisitos

- Node.js e npm instalados
- Backend executando em `http://localhost:8000`
- MongoDB iniciado, pois ele e necessario pelo backend

## Instalar e executar

Na primeira execucao, instale as dependencias:

```bash
cd /c/Projetos/from-scratch/frontend
npm install
```

Inicie o servidor de desenvolvimento:

```bash
npm run dev
```

Abra o endereco exibido no terminal, normalmente `http://localhost:5173`.

## Scripts disponiveis

```bash
npm run dev      # inicia o Vite com recarregamento automatico
npm run build    # cria a build de producao em dist/
npm run lint     # executa o Oxlint
npm run preview  # serve a build de producao localmente
```

## Estrutura

```text
frontend/
├── src/
│   ├── App.jsx     # tela e interacoes da lista de tarefas
│   ├── api.js      # cliente Axios e funcoes da API
│   ├── App.css     # estilos da aplicacao
│   └── main.jsx    # ponto de entrada do React
├── public/         # arquivos publicos
├── index.html      # documento HTML inicial
└── package.json    # dependencias e scripts
```

O endereco da API esta configurado em `src/api.js`. Se o backend for executado em outro endereco, atualize o `baseURL` nesse arquivo.

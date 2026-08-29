# Primeiro Projeto: App de Tarefas com React + FastAPI + MongoDB

**Data:** 2026-08-29  
**MVP:** App gerenciador de tarefas com tela responsiva e persistência em banco de dados  
**Stack escolhida:** React (frontend) + FastAPI (backend) + MongoDB (database)

---

## 📋 Resumo da Stack

| Camada | Tecnologia | Versão | Justificativa |
|--------|-----------|--------|---------------|
| **Frontend** | React | 18+ | Biblioteca popular, componentes reutilizáveis, grande comunidade |
| **Backend** | FastAPI | 0.100+ | Python moderno, async nativo, validação automática com Pydantic |
| **Database** | MongoDB | 6+ | NoSQL flexível, ótimo para prototipagem rápida, local ou via Atlas |
| **Package Manager (JS)** | npm | 11.17+ | Gerencia dependências do React |
| **Package Manager (Python)** | pip | 24+ | Gerencia dependências do FastAPI |
| **Version Control** | Git | 2.55+ | Já instalado, já integrado ao projeto |

---

## ✅ Seu Ambiente Atual

| Ferramenta | Status | Versão | Ação |
|-----------|--------|--------|------|
| Python | ✅ | 3.11.9 | Pronto |
| Node.js | ✅ | v24.19.0 | Pronto |
| npm | ✅ | 11.17.0 | Pronto |
| Git | ✅ | 2.55.0 | Pronto |
| **MongoDB** | ❌ | — | **INSTALAR** |
| Docker | ℹ️ | — | Opcional (facilita MongoDB) |

---

## 🚀 MongoDB: Três Formas de Usar

### Opção 1: MongoDB Local Direto (Recomendado para começar)

**Passos:**

```powershell
# 1. Instalar MongoDB Community Edition via winget
winget install --id MongoDB.Server

# 2. Verificar se instalou
mongod --version

# 3. Criar pasta de dados (se não existir)
mkdir C:\data\db

# 4. Iniciar servidor MongoDB em um terminal
mongod --dbpath C:\data\db

# 5. Em outro terminal, testar conexão
mongosh
```

**Vantagem:** Controle total, banco fica localmente.  
**Desvantagem:** Precisa de terminal extra rodando.

---

### Opção 2: MongoDB via Docker (Mais Profissional)

**Passos:**

```powershell
# 1. Instalar Docker Desktop (https://www.docker.com/products/docker-desktop)

# 2. Executar MongoDB em container
docker run --name mongodb -d -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=admin -e MONGO_INITDB_ROOT_PASSWORD=password mongo:latest

# 3. Verificar se está rodando
docker ps

# 4. Conectar com MongoDB Compass (GUI)
# URI: mongodb://admin:password@localhost:27017
```

**Vantagem:** Isolado, fácil remover.  
**Desvantagem:** Precisa de Docker instalado.

---

### Opção 3: MongoDB Atlas (Cloud - Sem Instalar)

**Passos:**

1. Ir para [https://www.mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
2. Criar conta gratuita (tier free: 512 MB)
3. Criar cluster
4. Copiar connection string
5. Usar na aplicação

**Vantagem:** Sem instalar, acesso de qualquer lugar.  
**Desvantagem:** Precisa de internet, limite de dados.

---

## 📂 Estrutura do Projeto

Você terá dois diretórios independentes (já criados):

```
c:\Projetos\
├── from-scratch/              # Código do projeto (React + FastAPI)
│   ├── .git/
│   ├── .specs/                # Especificações (este arquivo aqui)
│   ├── frontend/              # React app
│   │   ├── src/
│   │   ├── package.json
│   │   └── ...
│   └── backend/               # FastAPI
│       ├── main.py
│       ├── requirements.txt
│       └── ...
│
└── project-map/               # Documentação SDD (separado)
    ├── .specs/
    ├── plano-do-projeto.md
    └── ...
```

---

## 📦 Dependências por Camada

### Frontend (React)

```bash
# Será instalado via npm install
npm install react react-dom
npm install axios             # Cliente HTTP
npm install react-router-dom  # Roteamento (opcional)
```

### Backend (FastAPI)

```bash
# Será instalado via pip install -r requirements.txt
fastapi==0.100.0
uvicorn==0.24.0              # Servidor ASGI
pymongo==4.6.0               # Driver MongoDB
pydantic==2.4.0              # Validação
python-dotenv==1.0.0         # Variáveis de ambiente
```

### Banco de Dados

- **MongoDB Community:** Free, local ou cloud

---

## 🎯 MVP: App de Tarefas (Escopo Inicial)

### Funcionalidades Iniciais (Fase 1)

- ✅ **Criar tarefa:** formulário simples + salvar em MongoDB
- ✅ **Listar tarefas:** tela com tabela/cards de tarefas
- ✅ **Marcar como concluída:** toggle simples
- ✅ **Deletar tarefa:** botão com confirmação
- ✅ **Persistência:** dados salvam e carregam do banco

### Fora do MVP (Fases Futuras)

- 🔄 Editar tarefa
- 🔄 Filtrar por status (pendente/concluída)
- 🔄 Ordenar por data
- 🔄 Autenticação de usuário
- 🔄 Deploy em produção

---

## 🏗️ Arquitetura de Alto Nível

```
┌─────────────────────┐
│   Frontend: React   │  localhost:3000
│  - UI das tarefas   │
│  - Formulário       │
└──────────┬──────────┘
           │ HTTP (axios)
           ▼
┌─────────────────────┐
│  Backend: FastAPI   │  localhost:8000
│  - API REST         │  /api/tasks/
│  - Validação        │  /api/tasks/{id}
└──────────┬──────────┘
           │ Driver MongoClient
           ▼
┌─────────────────────┐
│    MongoDB Local    │  localhost:27017
│  - Database: tasks  │
│  - Collection: todo │
└─────────────────────┘
```

---

## ⚡ Próximos Passos

### 1. **INSTALAR MongoDB**
   - [ ] Escolher Opção 1 (Local), 2 (Docker), ou 3 (Atlas)
   - [ ] Testar conexão (`mongosh` ou MongoDB Compass)

### 2. **CRIAR Backend (FastAPI)**
   - [ ] Criar pasta `backend/`
   - [ ] Criar `requirements.txt`
   - [ ] Criar `main.py` com rotas iniciais

### 3. **CRIAR Frontend (React)**
   - [ ] Criar app com `npx create-react-app frontend`
   - [ ] Ou usar Vite: `npm create vite@latest frontend -- --template react`
   - [ ] Conectar ao backend via `axios`

### 4. **ESPECIFICAR FEATURES** (com tlc-spec-driven)
   - [ ] `/tlc-spec-driven specify feature: criar tarefa`
   - [ ] `/tlc-spec-driven specify feature: listar tarefas`
   - [ ] `/tlc-spec-driven implement` para cada feature

---

## 🔗 Referências

- **React:** https://react.dev
- **FastAPI:** https://fastapi.tiangolo.com
- **MongoDB Driver (Python):** https://docs.mongodb.com/drivers/pymongo
- **Axios:** https://axios-http.com

---

## 📝 Decisões Registradas

| Decisão | Valor | Justificativa |
|---------|-------|---------------|
| Framework Frontend | React | Popular, curva aprendizado moderada |
| Framework Backend | FastAPI | Python moderno, async nativo |
| Banco de Dados | MongoDB | Flexível, ótimo para MVP |
| Banco Local | Opção 1 (instalado) | Mais simples para começar |
| MVP Escopo | 5 features core | Tarefas CRUD + persistência |

---

**Status:** Pronto para começar. Próximo passo: Instalar MongoDB e inicializar backend.

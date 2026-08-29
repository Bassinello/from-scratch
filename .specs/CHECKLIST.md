# 🚀 Checklist: Instalação do Ambiente

**Objetivo:** Validar e instalar tudo que falta para começar o primeiro projeto.

---

## ✅ FASE 1: Validar o que já está instalado

- [x] Python 3.11.9 ✅
- [x] Node.js v24.19.0 ✅
- [x] npm 11.17.0 ✅
- [x] Git 2.55.0 ✅
- [ ] **MongoDB** ❌ (INSTALAR)

---

## 📥 FASE 2: Instalar MongoDB

### Opção Recomendada: MongoDB Local (Mais Simples)

**Passo 1:** Abra PowerShell como Administrador

```powershell
# Digitar no PowerShell (como Administrador)
winget install --id MongoDB.Server
```

⏳ Aguarde a instalação (~ 2 minutos)

**Passo 2:** Verifique a instalação

```powershell
mongod --version
```

Deve aparecer algo como: `db version v7.0.0` ou similar.

**Passo 3:** Crie a pasta de dados

```powershell
mkdir C:\data\db
```

**Passo 4:** Inicie o servidor MongoDB

```powershell
# Terminal 1: Deixe rodando
mongod --dbpath C:\data\db
```

Deve aparecer: `Waiting for connections on port 27017`

**Passo 5:** Teste a conexão (em outro terminal)

```powershell
# Terminal 2
mongosh
```

Se aparecer `>` ou `test>`, está funcionando! Aperte `exit` para sair.

---

### Alternativa: MongoDB via Docker

Se prefere isolar em container:

```powershell
# 1. Instalar Docker Desktop
# https://www.docker.com/products/docker-desktop

# 2. Inicie MongoDB em Docker
docker run --name mongodb -d -p 27017:27017 mongo

# 3. Teste
docker exec -it mongodb mongosh
```

---

## 🎯 FASE 3: Validar Python + pip

```powershell
python3 --version     # Deve mostrar Python 3.11.9
pip --version         # Deve mostrar pip 24.x
```

Se `pip` não funcionar:

```powershell
python3 -m pip --version
```

---

## 📦 FASE 4: Preparar Backend (FastAPI)

```powershell
# Na pasta do projeto
cd c:\Projetos\from-scratch

# Criar pasta backend
mkdir backend
cd backend

# Criar arquivo requirements.txt
```

**Conteúdo de `requirements.txt`:**

```
fastapi==0.104.1
uvicorn==0.24.0
pymongo==4.6.0
pydantic==2.5.0
pydantic-settings==2.1.0
python-dotenv==1.0.0
cors==1.0.1
```

Depois, instale:

```powershell
pip install -r requirements.txt
```

---

## ⚛️ FASE 5: Preparar Frontend (React)

```powershell
# Na pasta do projeto
cd c:\Projetos\from-scratch

# Criar app React com Vite (mais rápido)
npm create vite@latest frontend -- --template react

# Ou com create-react-app (mais pesado)
npx create-react-app frontend

# Instale dependências
cd frontend
npm install

# Teste se funciona
npm run dev
# Deve abrir http://localhost:5173
```

---

## 🔧 FASE 6: Estrutura Final

Ao final, você terá:

```
c:\Projetos\from-scratch\
├── .specs/
│   ├── PRIMEIRO_PROJETO.md       ← Você está aqui
│   └── CHECKLIST.md               ← Este arquivo
├── backend/
│   ├── main.py                    (vazio por enquanto)
│   ├── requirements.txt
│   └── venv/                      (criado após pip install)
├── frontend/
│   ├── src/
│   ├── package.json
│   └── node_modules/
├── .git/
├── .gitignore
└── README.md
```

---

## ✨ FASE 7: Testar Tudo Junto

**Terminal 1: MongoDB rodando**
```powershell
mongod --dbpath C:\data\db
# Deixe aqui, não feche
```

**Terminal 2: Backend**
```powershell
cd c:\Projetos\from-scratch\backend
python3 main.py
# Ou
uvicorn main:app --reload
```

**Terminal 3: Frontend**
```powershell
cd c:\Projetos\from-scratch\frontend
npm run dev
```

Se tudo der certo:
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- MongoDB: localhost:27017

---

## 📋 Checklist Final

- [ ] MongoDB instalado e testado (`mongosh` funciona)
- [ ] Pasta `backend/` criada
- [ ] `requirements.txt` criado
- [ ] `pip install -r requirements.txt` executado com sucesso
- [ ] Pasta `frontend/` criada com React/Vite
- [ ] `npm install` executado no frontend
- [ ] `npm run dev` abre o app React
- [ ] Git inicializado (já está em from-scratch)

---

## 🚨 Problemas Comuns

| Problema | Solução |
|----------|---------|
| `mongod: command not found` | MongoDB não está no PATH. Reinicie o terminal ou instale novamente. |
| `npm: execution policy` | Use `npm.cmd` em vez de `npm` ou execute PowerShell como Admin |
| `pip: command not found` | Use `python3 -m pip` em vez de `pip` |
| `Port 27017 already in use` | Outro MongoDB está rodando. Feche-o ou mude a porta com `mongod --port 27018` |
| `Cannot find module 'fastapi'` | Execute `pip install fastapi` novamente |

---

**Próximo passo após completar este checklist:** Abra o arquivo `.specs/PRIMEIRO_PROJETO.md` e comece a especificar as features com `/tlc-spec-driven`

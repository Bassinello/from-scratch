# STATE.md - Projeto: Gerenciador de Tarefas (Task Manager)

**Última atualização:** 2026-08-29  
**Status:** ⏸️ PAUSADO - MVP completo (Backend OK, Frontend OK) - falta validação E2E manual

---

## 📍 HANDOFF SNAPSHOT

### Branches e Commits
- **Branch:** main
- **Último commit:** `f292d2f` - "feat: cria frontend React com Vite e componente de tarefas conectado a API"
- **Remote:** origin/main (GitHub Bassinello/from-scratch)

### Estado de Trabalho
- **Arquivos modificados:** Nenhum (working tree clean)
- **Alterações staged:** Nenhum
- **Branches não merged:** Nenhum

### Dependências Instaladas
```
Backend:
  fastapi==0.141.1
  uvicorn==0.52.4
  pymongo==4.17.0
  pydantic==2.13.5
  python-dotenv==1.0.0

Frontend:
  (ainda não finalizado)
```

### Serviços Ativos
- ✅ MongoDB 8.3.7 rodando em localhost:27017
- ✅ FastAPI uvicorn rodando em http://localhost:8000
- ⏳ Frontend (iniciado, estrutura base criada)

---

## 🏗️ ESPECIFICAÇÕES (MVP)

### Feature 1: Criar Tarefa

**REQ-001: Usuário deve criar tarefa com título e descrição**

| Critério de Aceite | Status |
|-------------------|--------|
| AC-001: Endpoint POST /api/tasks aceita `title` e `description` obrigatórios | ✅ DONE |
| AC-002: Sistema salva tarefa em MongoDB com `_id`, `created_at`, `completed=false` | ✅ DONE |
| AC-003: Endpoint retorna tarefa criada com código 201 | ✅ DONE |
| AC-004: Validação rejeita title vazio ou description vazia | ✅ DONE |

**Escopo:** Small (≤ 3 arquivos, lógica simples)  
**Fases:** Specify ✅ + Execute ✅ (Design e Tasks pulados)

---

### Feature 2: Listar Tarefas

**REQ-002: Usuário deve listar todas as tarefas**

| Critério de Aceite | Status |
|-------------------|--------|
| AC-001: Endpoint GET /api/tasks retorna array de tarefas | ✅ DONE |
| AC-002: Tarefas mostram todos os campos (_id, title, description, completed, created_at) | ✅ DONE |
| AC-003: Lista está vazia se banco vazio, retorna [] | ✅ DONE |
| AC-004: Endpoint retorna código 200 | ✅ DONE |

**Escopo:** Small  
**Fases:** Specify ✅ + Execute ✅

---

### Feature 3: Marcar Tarefa como Concluída

**REQ-003: Usuário deve marcar tarefa como concluída**

| Critério de Aceite | Status |
|-------------------|--------|
| AC-001: Endpoint PATCH /api/tasks/{id} aceita `completed: boolean` | ✅ DONE |
| AC-002: Atualiza campo `completed` da tarefa no MongoDB | ✅ DONE |
| AC-003: Retorna tarefa atualizada | ✅ DONE |
| AC-004: Rejeita ID inválido com erro 404 | ✅ DONE |

**Escopo:** Small  
**Fases:** Specify ✅ + Execute ✅

---

### Feature 4: Deletar Tarefa

**REQ-004: Usuário deve deletar tarefa**

| Critério de Aceite | Status |
|-------------------|--------|
| AC-001: Endpoint DELETE /api/tasks/{id} remove tarefa | ✅ DONE |
| AC-002: Retorna código 204 (No Content) | ✅ DONE |
| AC-003: Rejeita ID inválido com erro 404 | ✅ DONE |

**Escopo:** Small  
**Fases:** Specify ✅ + Execute ✅

---

### Feature 5: Health Check

**REQ-005: Sistema deve reportar saúde**

| Critério de Aceite | Status |
|-------------------|--------|
| AC-001: Endpoint GET /health verifica API | ✅ DONE |
| AC-002: Endpoint GET /health verifica MongoDB | ✅ DONE |
| AC-003: Retorna status JSON | ✅ DONE |

**Escopo:** Small  
**Fases:** Specify ✅ + Execute ✅

---

## ✅ TAREFAS EXECUTADAS

### Backend (Fase: Execute) ✅

| # | Tarefa | Status | Commit |
|---|--------|--------|--------|
| T-001 | Setup FastAPI + Uvicorn | ✅ | múltiplos |
| T-002 | Conectar MongoDB com pymongo | ✅ | múltiplos |
| T-003 | Definir modelos Pydantic (Task, TaskCreate, TaskUpdate) | ✅ | 87a032a |
| T-004 | Implementar POST /api/tasks (CREATE) | ✅ | múltiplos |
| T-005 | Implementar GET /api/tasks (LIST) | ✅ | múltiplos |
| T-006 | Implementar GET /api/tasks/{id} (READ) | ✅ | múltiplos |
| T-007 | Implementar PATCH /api/tasks/{id} (UPDATE) | ✅ | múltiplos |
| T-008 | Implementar DELETE /api/tasks/{id} | ✅ | múltiplos |
| T-009 | Adicionar CORS middleware | ✅ | múltiplos |
| T-010 | Adicionar Health Check endpoints | ✅ | múltiplos |
| T-011 | Corrigir validadores Pydantic v2 | ✅ | 87a032a |
| T-012 | Adicionar serializador ObjectId (JSON) | ✅ | 87a032a |

**Testes:** ✅ Todos os endpoints testados e funcionando (curl/httpie)

---

### Frontend (Fase: Execute) ✅

| # | Tarefa | Status | Arquivo |
|---|--------|--------|---------|
| T-013 | Criar estrutura base React com Vite | ✅ | frontend/ |
| T-014 | Instalar dependências (react, axios, etc) | ✅ | package.json |
| T-015 | Criar cliente API (axios) | ✅ | frontend/src/api.js |
| T-016 | Implementar componente de tarefas (listar/criar/concluir/excluir) | ✅ | frontend/src/App.jsx |
| T-017 | Estilizar lista de tarefas | ✅ | frontend/src/App.css |
| T-018 | Validar build de produção (vite build) | ✅ | — |

**Testes:** ✅ Build de produção passou sem erros (`vite build` - 73 módulos, 449ms)

---

## 🛠️ DECISÕES REGISTRADAS

### Decision AD-001: Framework Frontend
**Contexto:** Escolher entre React, Vue, Svelte  
**Decisão:** **React 18+**  
**Justificativa:** Popular, comunidade grande, mais recursos para iniciante  
**Data:** 2026-08-29

### Decision AD-002: Database Backend
**Contexto:** MongoDB local vs Docker vs Atlas  
**Decisão:** **MongoDB Local (instalado via winget)**  
**Justificativa:** Simplicidade, sem dependências extras, bom para MVP  
**Data:** 2026-08-29

### Decision AD-003: Backend Framework
**Contexto:** FastAPI vs Flask vs Django  
**Decisão:** **FastAPI 0.141.1**  
**Justificativa:** Async nativo, validação automática Pydantic, documentação automática  
**Data:** 2026-08-29

### Decision AD-004: MVP Scope
**Contexto:** Quantas features no MVP?  
**Decisão:** **5 features core: CREATE, READ-LIST, READ-ID, UPDATE, DELETE, HEALTH**  
**Justificativa:** Cobertura CRUD completa + validação de saúde  
**Data:** 2026-08-29

---

## 📊 ANDAMENTO

### Backend: ✅ 100% COMPLETO

```
Tarefas: 12/12 done
Endpoints: 7/7 implementados (POST, GET-list, GET-id, PATCH, DELETE, health, root)
Testes: Validados manualmente (curl)
Documentação: Inline no código
```

**O que funciona:**
- ✅ Conexão MongoDB automática no startup
- ✅ Validação Pydantic em todos os endpoints
- ✅ CORS habilitado para localhost:5173 e 3000
- ✅ Serialização ObjectId → JSON
- ✅ Error handling com códigos HTTP apropriados

---

### Frontend: ✅ 100% MVP COMPLETO

```
Setup: ✅ Vite + React 19
Componentes: ✅ App.jsx (form + lista + toggle + delete)
API Client: ✅ axios (api.js)
Build: ✅ vite build passou (449ms)
Testes: ⏳ Manual apenas (sem E2E ainda)
```

**O que foi feito:**
- ✅ Scaffold Vite + React 19
- ✅ axios instalado e configurado (baseURL localhost:8000)
- ✅ Componente único `App.jsx` com CRUD completo (create, list, toggle, delete)
- ✅ CSS simplificado para lista de tarefas
- ✅ Build de produção validado

**O que falta (não-MVP):**
- [ ] Rodar `npm run dev` e validar E2E com backend rodando
- [ ] Separar em componentes menores (TaskList, TaskForm, TaskItem) se crescer
- [ ] Testes automatizados
- [ ] Estilização avançada

---

## 🎯 PRÓXIMOS PASSOS (Ordem Recomendada)

### Fase 1: Validação E2E Manual (Próxima)
```
1. Terminal 1: MongoDB rodando
2. Terminal 2: cd backend && python3 -m uvicorn main:app --reload
3. Terminal 3: cd frontend && npm run dev
4. Abrir http://localhost:5173 e testar criar/listar/concluir/excluir
```

### Fase 2: Testes Backend (Opcional)
```
1. Criar test_main.py com pytest
2. Adicionar CI/CD (GitHub Actions)
3. Coverage report
```

### Fase 3: Deploy (Futuro)
```
1. Dockerfile para backend
2. Vercel/Netlify para frontend
3. MongoDB Atlas (cloud)
```

---

## 📝 CONTEXTO TÉCNICO

### Backend Stack
```python
# main.py
FastAPI app com 7 endpoints:
- GET / (health root)
- GET /health (health check com MongoDB)
- POST /api/tasks (criar)
- GET /api/tasks (listar)
- GET /api/tasks/{id} (pegar por ID)
- PATCH /api/tasks/{id} (atualizar)
- DELETE /api/tasks/{id} (deletar)

# models.py
Pydantic v2 models:
- Task (com ObjectId customizado)
- TaskCreate
- TaskUpdate

# database.py
PyMongo connection:
- MongoClient(localhost:27017)
- Database: "task_db"
- Collection: "tasks"
```

### Frontend Stack (Esperado)
```javascript
// App.jsx
React app com componentes:
- TaskList (listagem)
- TaskForm (criar/editar)
- TaskItem (card individual)

// api.js
Axios client:
- GET /api/tasks
- POST /api/tasks
- PATCH /api/tasks/{id}
- DELETE /api/tasks/{id}
```

---

## 🔗 Arquivos Críticos

| Arquivo | Linha | Descrição |
|---------|------|-----------|
| backend/main.py | L1-50 | Endpoints definidos |
| backend/models.py | — | Schemas Pydantic |
| backend/database.py | — | Conexão MongoDB |
| .specs/PRIMEIRO_PROJETO.md | — | Especificação completa |
| .specs/CHECKLIST.md | — | Guia de instalação |
| .specs/STATUS_INSTALACAO.md | — | Status do ambiente |

---

## 🚨 PROBLEMAS CONHECIDOS E RESOLVIDOS

| Problema | Solução | Status |
|----------|---------|--------|
| PyObjectId não compatível com Pydantic v2 | Usar `ConfigDict` + `StrSchema` | ✅ FIXED |
| ObjectId não serializável para JSON | Adicionar custom encoder no FastAPI | ✅ FIXED |
| CORS bloqueando frontend local | Adicionar middleware CORSMiddleware | ✅ FIXED |
| MongoDB não no PATH | Adicionar à variável PATH do Windows | ✅ FIXED |

---

## 📚 DOCUMENTAÇÃO DISPONÍVEL

- [PRIMEIRO_PROJETO.md](.specs/PRIMEIRO_PROJETO.md) — Stack e arquitetura
- [CHECKLIST.md](.specs/CHECKLIST.md) — Passo-a-passo instalação
- [STATUS_INSTALACAO.md](.specs/STATUS_INSTALACAO.md) — Status do ambiente
- [README.md](../README.md) — Overview do projeto

---

## 🔄 COMO RETOMAR

### 1. Verificar Estado
```bash
git status                    # Deve estar clean
git log --oneline -5          # Ver commits recentes
```

### 2. Ativar Ambiente
```bash
# Terminal 1: MongoDB
& "C:\Program Files\MongoDB\Server\8.3\bin\mongod.exe" --dbpath C:\data\db

# Terminal 2: Backend
cd backend
python3 -m uvicorn main:app --reload

# Terminal 3: Frontend (próximo passo)
cd frontend
npm install
npm run dev
```

### 3. Testar Backend
```bash
curl http://localhost:8000/health
curl -X GET http://localhost:8000/api/tasks
```

---

**STATUS GERAL:** ✅ Backend pronto, Frontend em setup  
**PRÓXIMA AÇÃO:** Completar instalação frontend e conectar ao backend  
**TEMPO ESTIMADO:** 1-2 horas para frontend + testes

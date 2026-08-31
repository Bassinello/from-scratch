# Tasks de Autenticação

## Execution Protocol (OBRIGATÓRIO -- não pule)

Implemente estas tasks com a skill `tlc-spec-driven`: **ative-a pelo nome e siga seu fluxo de Execute e as Critical Rules.** Não procure os arquivos da skill por caminho de sistema de arquivos. A skill é a fonte de verdade para o fluxo completo (ciclo por task, delegação em sub-agentes, revisão de adesão, Verifier, sensor de discriminação).

---

**Design**: `.specs/features/auth/design.md`
**Status**: Aprovado

---

## Test Coverage Matrix

> Gerado a partir do código (não havia infra de testes anterior) + spec.md. Diretrizes encontradas: nenhuma — padrões fortes aplicados, elevados por pedido explícito do usuário (pytest no backend + Vitest/RTL no frontend).

| Camada de Código | Tipo de Teste Exigido | Expectativa de Cobertura | Padrão de Localização | Comando |
| --- | --- | --- | --- | --- |
| `backend/security.py` (utils de hash/token) | unit | Round-trip de hash/verify, senha errada rejeitada, unicidade/formato do token | `backend/tests/test_security.py` | `cd backend; python -m pytest tests/test_security.py -q` |
| `backend/main.py` rotas de auth | integration | Caminho feliz + cada caso de borda listado + caminho de erro por AUTH-01..08 | `backend/tests/test_auth.py` | `cd backend; python -m pytest tests/test_auth.py -q` |
| `backend/main.py` rotas de tarefas (autorização) | integration | Feliz + 401/403/404/422 por TASK-01..06 | `backend/tests/test_tasks_auth.py` | `cd backend; python -m pytest -q` |
| `frontend/src/LoginForm.jsx`, `RegisterForm.jsx` | unit | Renderização, submit, erro de validação, estados de erro do servidor | `frontend/src/*.test.jsx` | `cd frontend; npm run test:run` |
| `frontend/src/App.jsx` (gating de auth) | unit | Mostra login quando deslogado, tarefas quando logado, logout reseta a view | `frontend/src/App.test.jsx` | `cd frontend; npm run test:run` |
| `backend/models.py`, `backend/database.py`, arquivos de config | none | Apenas gate de build | — | build gate |

## Gate Check Commands

| Nível de Gate | Quando Usar | Comando |
| --- | --- | --- |
| Quick | Após uma task só com testes unitários de backend | `cd backend; python -m pytest tests/test_security.py -q` |
| Full (backend) | Após uma task com testes de integração de backend | `cd backend; python -m pytest -q` |
| Full (frontend) | Após uma task com testes unitários de frontend | `cd frontend; npm run test:run` |
| Build | Conclusão de fase / task só de config | `cd backend; python -m pytest -q` `;` `cd frontend; npm run lint; npm run build; npm run test:run` |

---

## Execution Plan

As fases são ordenadas e rodam sequencialmente - cada fase termina antes da próxima começar.

### Phase 0: Infraestrutura de Testes

```
T1 → T2
```

### Phase 1: Fundação de Dados e Segurança no Backend

```
T3 → T4 → T5 → T6 → T7 → T8 → T9
```

### Phase 2: Endpoints de Autenticação no Backend

```
T10 → T11 → T12 → T13 → T14 → T15
```

### Phase 3: Autorização de Tarefas no Backend

```
T16 → T17 → T18 → T19
```

### Phase 4: Autenticação no Frontend

```
T20 → T21 → T22 → T23
```

### Phase 5: UI de Visibilidade de Tarefas no Frontend

```
T24 → T25 → T26
```

---

## Task Breakdown

### T1: Infraestrutura de testes do backend (pytest + fixture de banco de teste)

**O quê**: Adicionar `pytest`, `httpx`, `passlib[bcrypt]`, `email-validator` a `backend/requirements.txt`; criar `backend/tests/conftest.py` com uma fixture `client` (FastAPI `TestClient`) apontando para um banco de teste isolado (`tasks_db_test`) via override de env, e uma fixture de limpeza que apaga as collections de teste após cada teste.
**Where**: `backend/requirements.txt`, `backend/tests/conftest.py`, `backend/tests/__init__.py`
**Depends on**: None
**Reaproveita**: padrão de conexão de `backend/database.py`
**Requisito**: N/A (infra)

**Ferramentas**: MCP: NONE / Skill: NONE

**Pronto quando**:
- [ ] `requirements.txt` inclui `pytest`, `httpx`, `passlib[bcrypt]`, `email-validator`
- [ ] `conftest.py` fornece uma fixture `client` usando `tasks_db_test` (nunca o banco de dev)
- [ ] Rodar `pytest` com zero arquivos de teste coleta com sucesso (sem erros de import)

**Tests**: none
**Gate**: build

---

### T2: Infraestrutura de testes do frontend (Vitest + RTL)

**O quê**: Adicionar `vitest`, `@testing-library/react`, `@testing-library/jest-dom`, `jsdom` às devDependencies de `frontend/package.json`; adicionar um bloco de config `test` em `vite.config.js`; criar `frontend/src/test/setup.js` (matchers do jest-dom); adicionar os scripts `"test": "vitest"` e `"test:run": "vitest run"`.
**Where**: `frontend/package.json`, `frontend/vite.config.js`, `frontend/src/test/setup.js`
**Depends on**: T1
**Reaproveita**: config existente do Vite
**Requisito**: N/A (infra)

**Ferramentas**: MCP: NONE / Skill: NONE

**Pronto quando**:
- [ ] `npm run test:run` executa com zero arquivos de teste e sai com código 0
- [ ] O bloco `test` de `vite.config.js` referencia `./src/test/setup.js` e `environment: "jsdom"`

**Tests**: none
**Gate**: build

---

### T3: Utilitário de hash de senha

**O quê**: `backend/security.py` — `hash_password(password: str) -> str` e `verify_password(password: str, password_hash: str) -> bool` usando `passlib.context.CryptContext(schemes=["bcrypt"])`.
**Where**: `backend/security.py`, `backend/tests/test_security.py`
**Depends on**: T2
**Reaproveita**: nada existente (módulo novo)
**Requisito**: AUTH-01 (AC4: senha nunca em texto puro)

**Ferramentas**: MCP: NONE / Skill: NONE

**Pronto quando**:
- [ ] `hash_password("x")` retorna uma string de hash bcrypt diferente da entrada
- [ ] `verify_password("x", hash_password("x"))` é `True`
- [ ] `verify_password("wrong", hash_password("x"))` é `False`

**Tests**: unit
**Gate**: quick

---

### T4: Utilitários de token de sessão

**O quê**: `backend/security.py` — `new_session_token() -> str` (`secrets.token_urlsafe(32)`) e `hash_token(token: str) -> str` (digest SHA-256 em hex).
**Where**: `backend/security.py` (mesmo arquivo, aditivo), `backend/tests/test_security.py` (mesmo arquivo, aditivo)
**Depends on**: T3
**Reaproveita**: módulo `backend/security.py` da T3
**Requisito**: design.md → Decisões Técnicas (armazenamento de sessão)

**Ferramentas**: MCP: NONE / Skill: NONE

**Pronto quando**:
- [ ] `new_session_token()` retorna uma string URL-safe não vazia; duas chamadas retornam valores diferentes
- [ ] `hash_token(t)` é determinístico (mesma entrada → mesma saída) e difere de `t`

**Tests**: unit
**Gate**: quick

---

### T5: Modelos de usuário

**O quê**: `backend/models.py` — adicionar `UserCreate {username: str (3-30, ^[a-zA-Z0-9_]+$), password: str (min 8), email: EmailStr}`, `UserPublic {id, username, email, created_at}`, `UserInDB {..., password_hash}`.
**Where**: `backend/models.py`
**Depends on**: T4
**Reaproveita**: padrões `ConfigDict`/`Field` já existentes em `models.py`
**Requisito**: AUTH-01, AUTH-03

**Ferramentas**: MCP: NONE / Skill: NONE

**Pronto quando**:
- [ ] Modelos importáveis, sem erros do Pydantic
- [ ] `UserCreate(username="ab", password="x", email="not-an-email")` levanta `ValidationError` (coberto indiretamente pelos testes de rota da T10)

**Tests**: none (coberto via testes de rota da T10)
**Gate**: build

---

### T6: Formato do modelo de sessão

**O quê**: `backend/models.py` — documentar o formato de `Session` como um helper de construção de dict simples (sem modelo Pydantic exposto via API; formato apenas interno, conforme design.md).
**Where**: `backend/models.py`
**Depends on**: T5
**Reaproveita**: nada
**Requisito**: design.md → Modelos de Dados (Session)

**Ferramentas**: MCP: NONE / Skill: NONE

**Pronto quando**:
- [ ] Formato do documento Session (`_id`, `user_id`, `created_at`, `expires_at`) documentado como comentário/type alias ao lado de `UserInDB`

**Tests**: none
**Gate**: build

---

### T7: Estender modelos de Task com dono/visibilidade

**O quê**: `backend/models.py` — adicionar `visibility: Literal["personal", "public"]` (obrigatório) a `TaskCreate`; adicionar `owner_id: PyObjectId`, `owner_username: str`, `visibility: Literal["personal","public"]` a `Task`; `TaskUpdate` sem mudança (visibility não editável neste MVP — fora de escopo).
**Where**: `backend/models.py`
**Depends on**: T6
**Reaproveita**: `PyObjectId`, classes `Task`/`TaskCreate`/`TaskUpdate` existentes
**Requisito**: TASK-01, TASK-02, TASK-03

**Ferramentas**: MCP: NONE / Skill: NONE

**Pronto quando**:
- [ ] `TaskCreate(title="x")` sem `visibility` levanta `ValidationError` (coberto via testes de rota da T17)
- [ ] O modelo `Task` aceita `owner_id`, `owner_username`, `visibility`

**Tests**: none (coberto via testes de rota da T17)
**Gate**: build

---

### T8: Collections users/sessions + índices

**O quê**: `backend/database.py` — adicionar `users_collection`, `sessions_collection`; criar índices únicos em `users.username` e `users.email`; criar índice TTL em `sessions.expires_at` (`expireAfterSeconds=0`).
**Where**: `backend/database.py`
**Depends on**: T7
**Reaproveita**: conexão `client`/`db` existente
**Requisito**: AUTH-02 (unicidade), design.md → Decisões Técnicas (TTL)

**Ferramentas**: MCP: NONE / Skill: NONE

**Pronto quando**:
- [ ] `db.users.index_information()` mostra índices únicos em `username` e `email`
- [ ] `db.sessions.index_information()` mostra um índice TTL em `expires_at`

**Tests**: none
**Gate**: build

---

### T9: Migração de dados — limpar tarefas sem dono

**O quê**: Limpeza pontual, confirmada manualmente: documentar e fornecer um script pequeno `backend/scripts/migrate_clear_legacy_tasks.py` que apaga todos os documentos de `tasks` sem `owner_id`, imprimindo a contagem apagada. **Não executado automaticamente** — exige que o operador rode explicitamente e confirme.
**Where**: `backend/scripts/migrate_clear_legacy_tasks.py`
**Depends on**: T8
**Reaproveita**: `backend/database.py::tasks_collection`
**Requisito**: TASK-06

**Ferramentas**: MCP: NONE / Skill: NONE

**Pronto quando**:
- [ ] O script imprime uma confirmação antes de apagar (`input("Type YES to continue: ")`)
- [ ] O script apaga apenas documentos sem `owner_id` (`{"owner_id": {"$exists": False}}`)
- [ ] O script NÃO é chamado por nenhum teste ou caminho de CI (verificado via grep — sem referências em outro lugar)

**Tests**: none (script destrutivo; a confirmação manual é a salvaguarda, não um teste automatizado)
**Gate**: build

---

### T10: POST /api/auth/register

**O quê**: Nova rota `POST /api/auth/register` em `backend/main.py` — valida `UserCreate`, checa unicidade de username/email (409 com o nome do campo), hasheia a senha, insere o usuário, retorna `UserPublic` com `201`.
**Where**: `backend/main.py`, `backend/tests/test_auth.py`
**Depends on**: T9
**Reaproveita**: `security.py::hash_password`, idioma existente de rota/HTTPException
**Requisito**: AUTH-01, AUTH-02, AUTH-03

**Ferramentas**: MCP: NONE / Skill: NONE

**Pronto quando**:
- [ ] Payload válido → `201` + corpo sem `password`/`password_hash`
- [ ] Username duplicado → `409` `{"detail": "username already registered"}`
- [ ] Email duplicado → `409` `{"detail": "email already registered"}`
- [ ] Campos ausentes/inválidos → `422`
- [ ] Documento salvo tem `password_hash`, nunca `password`

**Tests**: integration
**Gate**: full

---

### T11: POST /api/auth/login

**O quê**: Nova rota `POST /api/auth/login` — verifica credenciais, cria um documento de sessão (`hash_token`, `user_id`, `created_at`, `expires_at = agora+24h`), seta o cookie `session_id` (httpOnly, `samesite="lax"`, `max_age=86400`) com o token puro, retorna `UserPublic` com `200`.
**Where**: `backend/main.py`, `backend/tests/test_auth.py`
**Depends on**: T10
**Reaproveita**: `security.py::verify_password`, `new_session_token`, `hash_token`
**Requisito**: AUTH-04, AUTH-05

**Ferramentas**: MCP: NONE / Skill: NONE

**Pronto quando**:
- [ ] Credenciais corretas → `200` + `Set-Cookie: session_id=...` presente + corpo da resposta sem campo de senha
- [ ] Senha errada → `401` `{"detail": "invalid username or password"}`
- [ ] Username desconhecido → `401` `{"detail": "invalid username or password"}` (mesma mensagem da senha errada)
- [ ] Documento de sessão em `sessions` tem `expires_at` ≈ agora + 24h (tolerância de alguns segundos)

**Tests**: integration
**Gate**: full

---

### T12: Dependency `get_current_user`

**O quê**: `backend/deps.py` — lê o cookie `session_id` da `Request`, hasheia, busca em `sessions` pelo hash com `expires_at > agora`, resolve e retorna `UserPublic`, ou levanta `HTTPException(401)` se o cookie estiver ausente, a sessão não for encontrada, ou estiver expirada.
**Where**: `backend/deps.py`, `backend/tests/test_auth.py`
**Depends on**: T11
**Reaproveita**: `security.py::hash_token`
**Requisito**: AUTH-07

**Ferramentas**: MCP: NONE / Skill: NONE

**Pronto quando**:
- [ ] Sem cookie → `401`
- [ ] Cookie com token desconhecido/inválido → `401`
- [ ] Cookie referenciando uma sessão expirada → `401`
- [ ] Cookie referenciando uma sessão válida → retorna o `UserPublic` correto

**Tests**: integration (via uma rota de teste protegida temporária ou via T13)
**Gate**: full

---

### T13: GET /api/auth/me

**O quê**: Nova rota `GET /api/auth/me` usando `Depends(get_current_user)`, retorna o `UserPublic` atual.
**Where**: `backend/main.py`, `backend/tests/test_auth.py`
**Depends on**: T12
**Reaproveita**: `get_current_user`
**Requisito**: AUTH-04 (teste independente), AUTH-07

**Ferramentas**: MCP: NONE / Skill: NONE

**Pronto quando**:
- [ ] Requisição logada → `200` + usuário correto
- [ ] Sem sessão → `401`

**Tests**: integration
**Gate**: full

---

### T14: POST /api/auth/logout

**O quê**: Nova rota `POST /api/auth/logout` usando `Depends(get_current_user)` — apaga o documento de sessão pelo hash do token, limpa o cookie `session_id`, retorna `204`.
**Where**: `backend/main.py`, `backend/tests/test_auth.py`
**Depends on**: T13
**Reaproveita**: `get_current_user`, `security.py::hash_token`
**Requisito**: AUTH-06

**Ferramentas**: MCP: NONE / Skill: NONE

**Pronto quando**:
- [ ] Logout logado → `204`, documento de sessão removido de `sessions`
- [ ] `GET /api/auth/me` seguinte com o mesmo cookie (agora inválido) → `401`
- [ ] Logout sem sessão → `401`

**Tests**: integration
**Gate**: full

---

### T15: Verificar CORS + integração de cookie ponta a ponta

**O quê**: Confirmar que a config de `CORSMiddleware` em `backend/main.py` funciona com requisições de cookie com credenciais (origens explícitas já setadas, `allow_credentials=True` já setado — adicionar um teste de regressão); atualizar a instância axios de `frontend/src/api.js` com `withCredentials: true` (a metade do frontend entra aqui pois é necessária para qualquer chamada de auth funcionar, mesmo que a maior parte do trabalho de UI seja na Phase 4).
**Where**: `backend/main.py` (só verificar, mudar apenas se necessário), `frontend/src/api.js`, `backend/tests/test_auth.py`
**Depends on**: T14
**Reaproveita**: middleware CORS existente, instância axios existente
**Requisito**: design.md → Riscos e Preocupações (cookie/CORS)

**Ferramentas**: MCP: NONE / Skill: NONE

**Pronto quando**:
- [ ] Um teste de integração faz login com header `Origin: http://localhost:5173` e confirma `Access-Control-Allow-Credentials: true` na resposta
- [ ] A instância axios de `frontend/src/api.js` tem `withCredentials: true`

**Tests**: integration
**Gate**: full

---

### T16: Proteger todas as rotas `/api/tasks*`

**O quê**: Adicionar `current_user: UserPublic = Depends(get_current_user)` a `list_tasks`, `create_task`, `get_task`, `update_task`, `delete_task`, `delete_all_tasks`.
**Where**: `backend/main.py`, `backend/tests/test_tasks_auth.py`
**Depends on**: T15
**Reaproveita**: `get_current_user`
**Requisito**: AUTH-07

**Ferramentas**: MCP: NONE / Skill: NONE

**Pronto quando**:
- [ ] Chamar qualquer rota `/api/tasks*` sem sessão → `401`
- [ ] Chamar com sessão válida → passa da checagem de auth (comportamento existente inalterado nesta task)

**Tests**: integration
**Gate**: full

---

### T17: Estampar dono + exigir visibility na criação

**O quê**: `create_task` exige `visibility` (via `TaskCreate`, já imposto pelo modelo da T7) e estampa `owner_id`/`owner_username` a partir de `current_user` antes de inserir.
**Where**: `backend/main.py`, `backend/tests/test_tasks_auth.py`
**Depends on**: T16
**Reaproveita**: `TaskCreate` da T7
**Requisito**: TASK-01, TASK-02

**Ferramentas**: MCP: NONE / Skill: NONE

**Pronto quando**:
- [ ] Criar com `visibility="personal"` salva `owner_id`/`owner_username` de quem chamou e `visibility="personal"`
- [ ] Criar com `visibility="public"` salva o mesmo mas `visibility="public"`
- [ ] `visibility` ausente/inválido → `422`

**Tests**: integration
**Gate**: full

---

### T18: Filtrar listagem por dono/visibilidade

**O quê**: A query de `list_tasks` passa a ser `{"$or": [{"owner_id": current_user.id}, {"visibility": "public"}]}`; a resposta inclui `owner_username`/`visibility` por item (já no modelo `Task` da T7).
**Where**: `backend/main.py`, `backend/tests/test_tasks_auth.py`
**Depends on**: T17
**Reaproveita**: modelo `Task`
**Requisito**: TASK-03

**Ferramentas**: MCP: NONE / Skill: NONE

**Pronto quando**:
- [ ] A listagem do usuário B inclui a tarefa pública do usuário A mas não a pessoal
- [ ] A listagem do usuário A inclui tanto suas tarefas pessoais quanto públicas

**Tests**: integration
**Gate**: full

---

### T19: Autorização de dono/visibilidade em update/delete

**O quê**: `update_task`/`delete_task` buscam a tarefa primeiro (404 se não existir), depois checam `task["visibility"] == "public" or task["owner_id"] == current_user.id`; senão `403`.
**Where**: `backend/main.py`, `backend/tests/test_tasks_auth.py`
**Depends on**: T18
**Reaproveita**: estrutura existente de `update_task`/`delete_task`
**Requisito**: TASK-04, TASK-05

**Ferramentas**: MCP: NONE / Skill: NONE

**Pronto quando**:
- [ ] Dono editando/excluindo sua própria tarefa pessoal → sucesso
- [ ] Não-dono editando/excluindo tarefa pessoal de outro → `403`
- [ ] Qualquer usuário autenticado editando/excluindo uma tarefa pública (que não é sua) → sucesso
- [ ] Editar/excluir um id de tarefa inexistente → `404` (checado antes da checagem de dono)

**Tests**: integration
**Gate**: full

---

### T20: Cliente de API de auth no frontend

**O quê**: `frontend/src/api.js` — adicionar `register(user)`, `login(credentials)`, `logout()`, `getMe()`, todas passando pela instância axios com `withCredentials: true` (da T15).
**Where**: `frontend/src/api.js`, `frontend/src/api.test.js`
**Depends on**: T19
**Reaproveita**: padrão/instância axios existente
**Requisito**: AUTH-01, AUTH-04, AUTH-06

**Ferramentas**: MCP: NONE / Skill: NONE

**Pronto quando**:
- [ ] Cada função dispara o método/caminho correto (axios mockado) e retorna `res.data`

**Tests**: unit (axios mockado)
**Gate**: quick

---

### T21: Componente LoginForm

**O quê**: `frontend/src/LoginForm.jsx` — formulário controlado (username, password), chama `login()`, mostra um erro genérico em caso de falha, chama `onSuccess(user)` em caso de sucesso.
**Where**: `frontend/src/LoginForm.jsx`, `frontend/src/LoginForm.test.jsx`
**Depends on**: T20
**Reaproveita**: estilo/padrão de formulário existente em `App.jsx`
**Requisito**: AUTH-04, AUTH-05, AUTH-08

**Ferramentas**: MCP: NONE / Skill: NONE

**Pronto quando**:
- [ ] Renderiza os inputs de username/password e o botão de submit
- [ ] Submeter credenciais válidas chama `onSuccess` com o usuário retornado
- [ ] Submeter credenciais inválidas mostra a mensagem genérica de erro, não chama `onSuccess`

**Tests**: unit
**Gate**: quick

---

### T22: Componente RegisterForm

**O quê**: `frontend/src/RegisterForm.jsx` — formulário controlado (username, password, email), chama `register()`, mostra erros de campo/servidor, chama `onSuccess(user)` em caso de sucesso.
**Where**: `frontend/src/RegisterForm.jsx`, `frontend/src/RegisterForm.test.jsx`
**Depends on**: T21
**Reaproveita**: estilo/padrão de formulário existente em `App.jsx`
**Requisito**: AUTH-01, AUTH-02, AUTH-03

**Ferramentas**: MCP: NONE / Skill: NONE

**Pronto quando**:
- [ ] Renderiza os inputs de username/password/email e o botão de submit
- [ ] Submeter um username duplicado mostra a mensagem `409` do servidor
- [ ] Submeter dados válidos chama `onSuccess` com o usuário retornado

**Tests**: unit
**Gate**: quick

---

### T23: Bloquear `App.jsx` atrás da autenticação

**O quê**: `App.jsx` ganha estado `currentUser`/`authView`; renderiza `LoginForm`/`RegisterForm` (com um link de alternar entre eles) quando `currentUser` é `null`; renderiza a UI de tarefas existente + um botão de logout quando autenticado; ao montar, chama `getMe()` para restaurar o estado de sessão (se o cookie ainda for válido) em vez de sempre mostrar o login.
**Where**: `frontend/src/App.jsx`, `frontend/src/App.test.jsx`
**Depends on**: T22
**Reaproveita**: UI de tarefas existente em `App.jsx`
**Requisito**: AUTH-08

**Ferramentas**: MCP: NONE / Skill: NONE

**Pronto quando**:
- [ ] Renderização deslogada mostra só login/cadastro, nenhuma busca de tarefas é disparada
- [ ] Após login bem-sucedido, a UI de tarefas renderiza e `loadTasks()` é disparado
- [ ] Clicar em logout chama `logout()` e volta para a tela de login

**Tests**: unit
**Gate**: full

---

### T24: Seletor de visibilidade na criação de tarefa

**O quê**: Adicionar um select de `visibility` (`Pessoal` / `Pública`) ao formulário de criação de tarefa em `App.jsx`; incluído no payload de `createTask`.
**Where**: `frontend/src/App.jsx`, `frontend/src/App.test.jsx`
**Depends on**: T23
**Reaproveita**: formulário de criação de tarefa existente
**Requisito**: TASK-01, TASK-02

**Ferramentas**: MCP: NONE / Skill: NONE

**Pronto quando**:
- [ ] O formulário inclui um seletor de visibilidade com padrão "Pessoal"
- [ ] Submeter envia o valor de `visibility` selecionado para `createTask`

**Tests**: unit
**Gate**: quick

---

### T25: Badge de dono + visibilidade na lista de tarefas

**O quê**: Cada item da lista de tarefas mostra `owner_username` e um badge de visibilidade ("Pessoal"/"Pública").
**Where**: `frontend/src/App.jsx`, `frontend/src/App.css`, `frontend/src/App.test.jsx`
**Depends on**: T24
**Reaproveita**: renderização de lista de tarefas existente
**Requisito**: TASK-03

**Ferramentas**: MCP: NONE / Skill: NONE

**Pronto quando**:
- [ ] O texto do item renderizado inclui o username do dono e o rótulo de visibilidade

**Tests**: unit
**Gate**: full

---

### T26: Checklist manual de validação E2E

**O quê**: Checklist manual documentado (não automatizado) rodado quando todas as tasks anteriores estiverem verdes: (1) cadastrar usuário A e B, (2) A cria 1 tarefa pessoal + 1 pública, (3) B loga e vê só a pública, (4) B tenta editar a tarefa pessoal de A pela UI → vê um erro de permissão, (5) B edita a tarefa pública de A → sucesso, (6) fluxo de logout/login funciona para os dois usuários.
**Where**: `.specs/features/auth/tasks.md` (este checklist, anexado como registro concluído), sem arquivos de código
**Depends on**: T25
**Reaproveita**: servidores de dev rodando (`uvicorn`, `vite`)
**Requisito**: Critérios de Sucesso em spec.md

**Ferramentas**: MCP: NONE / Skill: NONE

**Pronto quando**:
- [ ] Os 6 passos do checklist acima passam manualmente com MongoDB/backend/frontend rodando juntos

**Tests**: none (manual)
**Gate**: build

---

## Phase Execution Map

```
Phase 0 → Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5

Phase 0:  T1 ------→ T2
Phase 1:  T3 ------→ T4 ------→ T5 ------→ T6 ------→ T7 ------→ T8 ------→ T9
Phase 2:  T10 -----→ T11 -----→ T12 -----→ T13 -----→ T14 -----→ T15
Phase 3:  T16 -----→ T17 -----→ T18 -----→ T19
Phase 4:  T20 -----→ T21 -----→ T22 -----→ T23
Phase 5:  T24 -----→ T25 -----→ T26
```

Execution is strictly sequential — one task at a time, in order. Total: 26 tasks / 6 phases → exceeds the ~8-task single-batch budget, so batch sub-agent delegation is offered at Execute start (see sub-agents.md packing rules): suggested packing is Batch 1 = Phase 0 + Phase 1 (9 tasks), Batch 2 = Phase 2 (6 tasks), Batch 3 = Phase 3 + Phase 4 (8 tasks), Batch 4 = Phase 5 (3 tasks).

### Cross-Phase Boundary Dependencies

The first task of each phase (after Phase 0) depends on the last task of the previous phase, since phases run sequentially:

```
T2 -> T3
T9 -> T10
T15 -> T16
T19 -> T20
T23 -> T24
```

---

## Task Granularity Check

| Task | Escopo | Status |
| --- | --- | --- |
| T1-T26 | Cada uma toca 1-3 arquivos fortemente coesos (implementação + seu próprio arquivo de teste) para uma entrega única | ✅ Granular |

## Diagram-Definition Cross-Check

| Task | Depende de (corpo da task) | Diagrama Mostra | Status |
| --- | --- | --- | --- |
| T1 | None | None | ✅ Match |
| T2 | T1 | T1→T2 | ✅ Match |
| T3 | T2 | T2→T3 (cross-phase) | ✅ Match |
| T4 | T3 | T3→T4 | ✅ Match |
| T5 | T4 | T4→T5 | ✅ Match |
| T6 | T5 | T5→T6 | ✅ Match |
| T7 | T6 | T6→T7 | ✅ Match |
| T8 | T7 | T7→T8 | ✅ Match |
| T9 | T8 | T8→T9 | ✅ Match |
| T10 | T9 | T9→T10 (cross-phase) | ✅ Match |
| T11 | T10 | T10→T11 | ✅ Match |
| T12 | T11 | T11→T12 | ✅ Match |
| T13 | T12 | T12→T13 | ✅ Match |
| T14 | T13 | T13→T14 | ✅ Match |
| T15 | T14 | T14→T15 | ✅ Match |
| T16 | T15 | T15→T16 (cross-phase) | ✅ Match |
| T17 | T16 | T16→T17 | ✅ Match |
| T18 | T17 | T17→T18 | ✅ Match |
| T19 | T18 | T18→T19 | ✅ Match |
| T20 | T19 | T19→T20 (cross-phase) | ✅ Match |
| T21 | T20 | T20→T21 | ✅ Match |
| T22 | T21 | T21→T22 | ✅ Match |
| T23 | T22 | T22→T23 | ✅ Match |
| T24 | T23 | T23→T24 (cross-phase) | ✅ Match |
| T25 | T24 | T24→T25 | ✅ Match |
| T26 | T25 | T25→T26 | ✅ Match |

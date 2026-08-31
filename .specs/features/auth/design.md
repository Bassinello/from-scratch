# Design de Autenticação

**Spec**: `.specs/features/auth/spec.md`
**Status**: Aprovado

---

## Visão Geral da Arquitetura

Adiciona uma camada de autenticação por sessão ao monólito de 2 camadas existente (FastAPI + MongoDB), sem introduzir novos serviços/containers.

```mermaid
graph TD
    Browser -->|POST credenciais| Login["POST /api/auth/login"]
    Login -->|bcrypt.verify| UsersColl[(users)]
    Login -->|cria sessão: hash(token)| SessionsColl[(sessions)]
    Login -->|Set-Cookie session_id=token httpOnly| Browser
    Browser -->|Cookie session_id| Protected["Rotas protegidas: /api/tasks*, /api/auth/me, /api/auth/logout"]
    Protected -->|hash(cookie) + checagem de expires_at| SessionsColl
    Protected -->|resolve usuário| UsersColl
    Protected -->|query owner_id/visibility| TasksColl[(tasks)]
```

---

## Análise de Reaproveitamento de Código

### Componentes Existentes a Aproveitar

| Componente | Localização | Como Usar |
| --- | --- | --- |
| `MongoClient` / `db` | `backend/database.py` | Estender com `users_collection`, `sessions_collection` |
| `PyObjectId` | `backend/models.py` | Reaproveitar para `User.id` e `Task.owner_id` |
| Padrão `TaskUpdate` (`exclude_unset`) | `backend/models.py` | Mesmo padrão de atualização parcial, reutilizável para futuras atualizações de usuário (não necessário agora, mas mesmo idioma) |
| Padrão de rotas/erros do FastAPI | `backend/main.py` | Novas rotas `/api/auth/*` seguem o mesmo idioma `HTTPException(status_code=..., detail=...)` já usado |
| Instância axios | `frontend/src/api.js` | Adicionar `withCredentials: true` e 3 novas chamadas, reaproveitando o padrão `.then((res) => res.data)` existente |

### Pontos de Integração

| Sistema | Método de Integração |
| --- | --- |
| Middleware CORS (`main.py`) | Já tem origens explícitas + `allow_credentials=True` — verificado como compatível com cookies, sem mudança necessária além de confirmar em uma task |
| Rotas CRUD de tarefas | `Depends(get_current_user)` adicionado a todas as rotas `/api/tasks*`; checagem de dono/visibilidade adicionada a `update_task`/`delete_task` |

---

## Componentes

### `backend/security.py` (NOVO)

- **Propósito**: Utilitários de hashing de senha e token de sessão, isolados da lógica de rotas.
- **Localização**: `backend/security.py`
- **Interfaces**:
  - `hash_password(password: str) -> str` — hash bcrypt via passlib
  - `verify_password(password: str, password_hash: str) -> bool`
  - `new_session_token() -> str` — `secrets.token_urlsafe(32)`
  - `hash_token(token: str) -> str` — digest SHA-256 em hex, usado como chave do documento em `sessions`
- **Dependências**: `passlib[bcrypt]`, stdlib `secrets`/`hashlib`
- **Reaproveita**: nada existente (conceito novo)

### `backend/models.py` (MODIFICADO)

- **Propósito**: Adicionar schemas de User/Session; estender schemas de Task com dono/visibilidade.
- **Novos modelos**: `UserCreate {username, password, email}`, `UserPublic {id, username, email, created_at}`, `UserInDB {..., password_hash}`
- **Modelos modificados**: `TaskCreate`/`Task` ganham `visibility: Literal["personal","public"]` (obrigatório em `TaskCreate`); `Task` ganha `owner_id: PyObjectId`, `owner_username: str`
- **Reaproveita**: padrões `PyObjectId`, `ConfigDict` já presentes no arquivo

### `backend/database.py` (MODIFICADO)

- **Propósito**: Expor `users_collection`, `sessions_collection`; criar os índices necessários na inicialização.
- **Interfaces**: `users_collection.create_index("username", unique=True)`, `users_collection.create_index("email", unique=True)`, `sessions_collection.create_index("expires_at", expireAfterSeconds=0)` (TTL — o Mongo apaga o documento quando `expires_at` < agora, já que o campo guarda um datetime absoluto)
- **Reaproveita**: conexão `client`/`db` existente

### `backend/deps.py` (NOVO)

- **Propósito**: dependency `get_current_user` do FastAPI, compartilhada por todas as rotas protegidas.
- **Interfaces**: `get_current_user(request: Request) -> UserPublic` — lê o cookie `session_id`, hasheia, busca em `sessions` pelo hash com `expires_at > agora`, resolve o usuário, ou levanta `HTTPException(401)`.
- **Dependências**: `backend/security.py::hash_token`, `backend/database.py`

### `backend/main.py` (MODIFICADO)

- **Propósito**: Novas rotas de autenticação; rotas de tarefas ganham auth + regras de dono/visibilidade.
- **Novas rotas**: `POST /api/auth/register`, `POST /api/auth/login`, `POST /api/auth/logout`, `GET /api/auth/me`
- **Rotas modificadas**: todas as `/api/tasks*` ganham `current_user: UserPublic = Depends(get_current_user)`; `create_task` estampa `owner_id`/`owner_username` e exige `visibility`; `list_tasks` filtra `{"$or": [{"owner_id": current_user.id}, {"visibility": "public"}]}`; `update_task`/`delete_task` checam `task.visibility == "public" or task.owner_id == current_user.id`, senão `403`

### `frontend/src/api.js` (MODIFICADO)

- **Propósito**: Chamadas de API de autenticação, sessão baseada em cookie.
- **Interfaces**: `register(user)`, `login(credentials)`, `logout()`, `getMe()`; a instância axios ganha `withCredentials: true`.

### `frontend/src/LoginForm.jsx` / `RegisterForm.jsx` (NOVO)

- **Propósito**: Formulários controlados de login/cadastro, espelhando o estilo de formulário já existente em `App.jsx`.
- **Interfaces**: `<LoginForm onSuccess={(user) => void} />`, `<RegisterForm onSuccess={(user) => void} />`

### `frontend/src/App.jsx` (MODIFICADO)

- **Propósito**: Bloquear a UI de tarefas atrás do estado `currentUser`; adicionar seletor de visibilidade e exibição do dono.
- **Novo estado**: `currentUser`, `authView` (`"login" | "register"`)
- **Comportamento**: `currentUser` nulo → renderiza `LoginForm`/`RegisterForm`; caso contrário → renderiza a UI de tarefas existente + botão de logout + seletor de visibilidade no formulário de criação + badge de dono/visibilidade em cada item da lista.

---

## Modelos de Dados

### User (Mongo `users`)

```python
{
  "_id": ObjectId,
  "username": str,       # índice único
  "email": str,          # índice único
  "password_hash": str,
  "created_at": datetime,
}
```

### Session (Mongo `sessions`)

```python
{
  "_id": str,            # digest sha256(token) em hex - a chave de busca
  "user_id": ObjectId,
  "created_at": datetime,
  "expires_at": datetime,  # índice TTL apaga o documento quando esse instante passa
}
```

### Task (Mongo `tasks`, atualizada)

```python
{
  "_id": ObjectId,
  "title": str,
  "description": str | None,
  "completed": bool,
  "owner_id": ObjectId,
  "owner_username": str,
  "visibility": "personal" | "public",
  "created_at": datetime,
  "updated_at": datetime,
}
```

**Relacionamentos**: `Task.owner_id` → `User._id` (sem FK imposta pelo Mongo; garantido pelo código da aplicação ao sempre estampar a partir da sessão autenticada). `Session.user_id` → `User._id`.

---

## Estratégia de Tratamento de Erros

| Cenário de Erro | Tratamento | Impacto no Usuário |
| --- | --- | --- |
| Username/email duplicado no cadastro | `409` com `{"detail": "username already registered"}` ou `{"detail": "email already registered"}` | Frontend mostra a mensagem exata |
| Payload de cadastro inválido | `422` (validação Pydantic) | Frontend mostra erro por campo |
| Username/senha errados no login | `401` com mensagem genérica `{"detail": "invalid username or password"}` | Frontend mostra erro genérico, nunca revela qual campo |
| Sessão ausente/expirada/inválida em rota protegida | `401` | Frontend redireciona para login |
| Não-dono editando/excluindo tarefa pessoal | `403` | Frontend mostra "você não tem permissão" |
| Tarefa não encontrada | `404` | Frontend mostra "tarefa não encontrada" |

---

## Riscos e Preocupações

| Preocupação | Localização | Impacto | Mitigação |
| --- | --- | --- | --- |
| Sem rate limiting em `/api/auth/login` | `backend/main.py` (rota nova) | Possibilita adivinhação de credenciais por força bruta | Fora de escopo neste MVP (documentado); revisitar se o app for exposto além de localhost |
| `pymongo` é síncrono dentro de rotas `async def` do FastAPI | `backend/database.py` (padrão pré-existente) | As rotas de auth somam mais chamadas síncronas ao Mongo por requisição, bloqueando o event loop sob carga | Aceito para o escopo do MVP (single-user/dev local); mesma mitigação futura do risco R-002 do project-map (migrar para `motor` se a carga aumentar) |
| Cookie de sessão exige configuração correta de credentials no CORS | Middleware CORS em `backend/main.py` | Uma configuração errada quebraria silenciosamente a persistência de login no navegador | CORS já usa origens explícitas + `allow_credentials=True`; verificado como parte de uma task da Fase 2, axios do frontend seta `withCredentials: true` |

> Nenhum outro risco encontrado além dos três acima.

---

## Decisões Técnicas

| Decisão | Escolha | Justificativa |
| --- | --- | --- |
| Hash de senha | bcrypt via `passlib[bcrypt]` | Padrão de mercado para apps FastAPI, fator de custo ajustável |
| Transporte de sessão | cookie httpOnly, token opaco | Confirmado com o usuário em vez de JWT; evita expor claims sensíveis no cliente |
| Armazenamento de sessão | Guardar `sha256(token)` no Mongo, nunca o token puro | Defesa em profundidade: um vazamento de leitura do banco não expõe tokens de sessão utilizáveis |
| Expiração de sessão | 24h fixas, índice TTL do Mongo + checagem explícita de `expires_at` na leitura | Simples, autolimpante, sem necessidade de job em background |
| Roteamento no frontend | Sem `react-router`; alternância de tela via estado local em `App.jsx` | Consistente com o estilo de componente único já usado, evita uma dependência nova para 3 telas |

> **Decisão de nível de projeto:** O padrão de sessão/cookie (token opaco + hash SHA-256 no servidor + índice TTL) estabelece uma convenção para qualquer feature futura que precise de sessão. Isso deve ser adicionado a `.specs/STATE.md` → `## Decisions` como `AD-006` assim que esta feature for implementada.


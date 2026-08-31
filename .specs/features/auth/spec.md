# Autenticação + Tarefas Pessoais/Públicas Specification

## Problem Statement

O app de tarefas hoje é single-user e sem autenticação: qualquer pessoa com acesso à API lê/escreve todas as tarefas. Para suportar múltiplos usuários, o sistema precisa de cadastro/login e de uma regra de visibilidade que separe tarefas pessoais (só o dono vê) de tarefas públicas (todos os usuários autenticados veem).

## Objetivos

- [ ] Usuário se cadastra com username, senha e email; username e email são únicos.
- [ ] Usuário loga com username + senha e recebe uma sessão válida por 24h (cookie httpOnly).
- [ ] A tela inicial (lista de tarefas) só é acessível após login.
- [ ] Ao criar uma tarefa, o usuário escolhe visibilidade: pessoal (só o dono vê) ou pública (todos veem).
- [ ] Tarefas pessoais só podem ser editadas/excluídas pelo dono; tarefas públicas podem ser editadas/excluídas por qualquer usuário autenticado.

## Out of Scope

| Feature | Reason |
| --- | --- |
| Reset de senha / "esqueci minha senha" | Não crítico para o MVP; requer envio de email |
| "Lembrar-me" / sessão além de 24h | Adiciona refresh token; fora do MVP |
| Rate limiting / proteção brute-force no login | Requer infra adicional; risco aceito (ver design.md → Risks) |
| Papéis/permissões (admin, moderador) | Todo usuário autenticado tem os mesmos privilégios |
| Edição de perfil (trocar senha/email) | Não pedido; feature futura |
| Grupos de compartilhamento seletivo | Só binário pessoal/público, sem grupos |

---

## Assumptions & Open Questions

| Assumption / decision | Chosen default | Rationale | Confirmed? |
| --- | --- | --- | --- |
| Duração da sessão | 24h fixas, sem renovação deslizante | Simplicidade; "lembrar-me" está fora de escopo | n |
| Tamanho mínimo de senha | 8 caracteres | Mínimo de mercado razoável | n |
| Formato de username | 3-30 chars, `[a-zA-Z0-9_]` | Evita colisão em cookies/URLs | n |
| Roteamento no frontend | Sem `react-router`; alternância de tela via estado local em `App.jsx` | Consistente com o estilo atual (componente único) | n |
| Rate limiting no login | Fora de escopo neste MVP | Ver Out of Scope | y |
| Tarefas existentes sem dono | Apagadas (limpar `tasks`) antes de subir a feature | Usuário escolheu explicitamente | y |

**Open questions:** none — todas resolvidas ou registradas acima.

---

## User Stories

### P1: Cadastro de usuário ⭐ MVP

**User Story**: Como visitante, quero me cadastrar com username, senha e email, para poder logar e usar o sistema de tarefas.

**Why P1**: Sem cadastro não há usuários para autenticar.

**Acceptance Criteria**:

1. WHEN o visitante submete cadastro com `username`, `password` e `email` válidos e não usados THEN o sistema SHALL criar o usuário com senha hasheada (bcrypt) e responder `201 Created`.
2. IF `username` ou `email` já existem THEN o sistema SHALL responder `409 Conflict` indicando qual campo está em conflito (`{"detail": "username already registered"}` ou `{"detail": "email already registered"}`).
3. IF `username`, `password` ou `email` estão ausentes, vazios, ou fora dos limites (`username`: 3-30 `[a-zA-Z0-9_]`; `password`: mínimo 8 caracteres; `email`: formato inválido) THEN o sistema SHALL responder `422 Unprocessable Entity`.
4. The system SHALL ALWAYS armazenar a senha apenas como hash bcrypt — nunca em texto puro.

**Independent Test**: Cadastrar um usuário novo via `POST /api/auth/register` e confirmar 201 + documento salvo com `password_hash` (não `password`).

---

### P1: Login ⭐ MVP

**User Story**: Como usuário cadastrado, quero logar com username e senha, para acessar minhas tarefas.

**Why P1**: Pré-requisito de tudo mais.

**Acceptance Criteria**:

1. WHEN o usuário submete `username` e `password` corretos THEN o sistema SHALL criar uma sessão, setar um cookie `session_id` (httpOnly, `SameSite=Lax`, `max_age=86400`) e responder `200 OK` com `{id, username, email, created_at}` (sem senha).
2. IF `username` não existe OU `password` está incorreta THEN o sistema SHALL responder `401 Unauthorized` com `{"detail": "invalid username or password"}` (mensagem genérica, nunca revela qual campo errou).
3. The system SHALL ALWAYS expirar a sessão 24h após a criação (`expires_at = now + 24h`).

**Independent Test**: Logar com credenciais válidas via `POST /api/auth/login`, confirmar cookie setado e `GET /api/auth/me` retornando o usuário logado.

---

### P1: Logout ⭐ MVP

**User Story**: Como usuário logado, quero sair da minha conta, para encerrar minha sessão neste dispositivo.

**Why P1**: Completa o ciclo de autenticação.

**Acceptance Criteria**:

1. WHEN o usuário logado submete `POST /api/auth/logout` THEN o sistema SHALL remover o registro da sessão em `sessions` e limpar o cookie no cliente, respondendo `204 No Content`.
2. IF o usuário não está logado (sem cookie/sessão válida) THEN o sistema SHALL responder `401 Unauthorized` ao tentar logout.

**Independent Test**: Logar, depois logout, depois tentar `GET /api/auth/me` → deve responder `401`.

---

### P1: Tela inicial protegida por login ⭐ MVP

**User Story**: Como usuário não autenticado, ao abrir o app quero ser levado à tela de login/cadastro.

**Why P1**: Pedido explícito do usuário.

**Acceptance Criteria**:

1. WHILE o usuário não está autenticado THE sistema SHALL exibir apenas as telas de login/cadastro (nenhuma tarefa é exibida ou buscada).
2. WHEN o login é bem-sucedido THEN o sistema SHALL exibir a tela de tarefas (lista + formulário de criação).
3. IF qualquer endpoint `/api/tasks*` é chamado sem sessão válida THEN o sistema SHALL responder `401 Unauthorized`.

**Independent Test**: Abrir o app deslogado → só vê login/cadastro; logar → vê a lista de tarefas.

---

### P1: Criar tarefa pessoal ou pública ⭐ MVP

**User Story**: Como usuário logado, quero escolher se uma tarefa é pessoal ou pública.

**Why P1**: Pedido explícito do usuário.

**Acceptance Criteria**:

1. WHEN o usuário logado cria uma tarefa com `visibility="personal"` THEN o sistema SHALL salvar a tarefa com `owner_id`/`owner_username` do usuário e `visibility="personal"`.
2. WHEN o usuário logado cria uma tarefa com `visibility="public"` THEN o sistema SHALL salvar a tarefa com `owner_id`/`owner_username` do usuário e `visibility="public"`.
3. IF `visibility` está ausente ou tem valor diferente de `"personal"`/`"public"` THEN o sistema SHALL responder `422 Unprocessable Entity`.

**Independent Test**: Criar uma tarefa pessoal e uma pública com o mesmo usuário; conferir os dois documentos no Mongo com `owner_id` e `visibility` corretos.

---

### P1: Listar tarefas visíveis para o usuário ⭐ MVP

**User Story**: Como usuário logado, quero ver minhas tarefas pessoais e todas as tarefas públicas, mas não as pessoais de outros.

**Why P1**: Regra central de visibilidade.

**Acceptance Criteria**:

1. WHEN o usuário logado lista tarefas (`GET /api/tasks`) THEN o sistema SHALL retornar suas próprias tarefas (qualquer visibility) + todas as tarefas de `visibility="public"` de qualquer usuário.
2. The system SHALL ALWAYS excluir da resposta tarefas `visibility="personal"` cujo `owner_id` seja diferente do usuário autenticado.
3. WHEN uma tarefa é retornada na listagem THEN o sistema SHALL incluir `owner_username` e `visibility`.

**Independent Test**: Usuário A cria 1 tarefa pessoal e 1 pública; usuário B loga e lista tarefas → vê só a pública de A (mais as suas próprias).

---

### P1: Autorização de edição/exclusão ⭐ MVP

**User Story**: Como usuário, quero que só eu possa mexer nas minhas tarefas pessoais, mas que qualquer usuário logado possa colaborar em tarefas públicas.

**Why P1**: Regra de negócio confirmada com o usuário.

**Acceptance Criteria**:

1. WHEN o dono de uma tarefa pessoal chama `PATCH`/`DELETE` nela THEN o sistema SHALL permitir a operação.
2. IF um usuário que não é o dono chama `PATCH`/`DELETE` em uma tarefa `visibility="personal"` de outro usuário THEN o sistema SHALL responder `403 Forbidden`.
3. WHEN qualquer usuário autenticado chama `PATCH`/`DELETE` em uma tarefa `visibility="public"` THEN o sistema SHALL permitir a operação.
4. IF a tarefa não existe THEN o sistema SHALL responder `404 Not Found` (checado depois da autenticação, antes da checagem de dono).

**Independent Test**: Usuário B tenta editar tarefa pessoal do usuário A → 403. Usuário B edita tarefa pública do usuário A → 200.

---

### P1: Migração dos dados existentes ⭐ MVP

**User Story**: Como responsável técnico, quero limpar as tarefas antigas (sem dono) antes de subir a feature.

**Why P1**: Decisão explícita do usuário; o novo schema exige `owner_id`/`visibility`.

**Acceptance Criteria**:

1. WHEN a migração é executada THEN o sistema SHALL remover todos os documentos da coleção `tasks` que não possuam `owner_id`.
2. The system SHALL ALWAYS exigir confirmação explícita do operador antes de rodar essa limpeza.

**Independent Test**: Rodar o script de migração e confirmar `tasks_collection.count_documents({}) == 0` antes dos testes da nova feature.

---

## Casos de Borda

- IF o cookie de sessão está presente mas expirado (>24h) THEN o sistema SHALL responder `401 Unauthorized`.
- IF o cookie de sessão referencia uma sessão que não existe mais (removida por logout) THEN o sistema SHALL responder `401 Unauthorized`.
- IF dois usuários tentam se cadastrar com o mesmo `username` simultaneamente THEN o índice único do MongoDB SHALL garantir que só um cadastro seja aceito; o segundo recebe `409`.
- WHEN um usuário já logado chama `/api/auth/register` ou `/api/auth/login` THEN o sistema SHALL permitir normalmente (sem bloqueio).
- IF o corpo de `POST /api/tasks` não inclui `title` THEN o sistema SHALL responder `422` (regra herdada do CRUD atual).

---

## Requirement Traceability

| Requirement ID | Story | Phase | Status |
| --- | --- | --- | --- |
| AUTH-01 | Cadastro de usuário (sucesso) | Tasks | Pending |
| AUTH-02 | Cadastro de usuário (conflito) | Tasks | Pending |
| AUTH-03 | Cadastro de usuário (validação) | Tasks | Pending |
| AUTH-04 | Login (sucesso) | Tasks | Pending |
| AUTH-05 | Login (credenciais inválidas) | Tasks | Pending |
| AUTH-06 | Logout | Tasks | Pending |
| AUTH-07 | Endpoints protegidos exigem sessão | Tasks | Pending |
| AUTH-08 | Tela inicial protegida por login | Tasks | Pending |
| TASK-01 | Criar tarefa pessoal | Tasks | Pending |
| TASK-02 | Criar tarefa pública | Tasks | Pending |
| TASK-03 | Listar tarefas visíveis | Tasks | Pending |
| TASK-04 | Autorização: pessoal só dono | Tasks | Pending |
| TASK-05 | Autorização: pública qualquer autenticado | Tasks | Pending |
| TASK-06 | Migração de dados existentes | Tasks | Pending |

**ID format:** `AUTH-NN` (autenticação/sessão), `TASK-NN` (visibilidade/autorização de tarefas)

**Status values:** Pending → In Design → In Tasks → Implementing → Verified

**Coverage:** 14 total, 14 mapped to tasks (ver tasks.md), 0 unmapped

---

## Critérios de Sucesso

- [ ] Um usuário novo consegue se cadastrar, logar, criar 1 tarefa pessoal e 1 pública, e ver ambas na sua lista.
- [ ] Um segundo usuário, ao logar, vê a tarefa pública do primeiro mas não a pessoal.
- [ ] Nenhuma senha é encontrada em texto puro no MongoDB.
- [ ] Tentar acessar `/api/tasks` sem estar logado sempre responde `401`.

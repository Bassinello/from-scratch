# Contexto de Autenticação

**Coletado em:** 2026-08-31
**Spec:** `.specs/features/auth/spec.md`
**Status:** Pronto para design

---

## Limite da Feature

Autenticação completa (registro/login/logout/sessão via cookie httpOnly) + regra pessoal/público em tarefas, com autorização de edição/exclusão. Nada além disso (ver Out of Scope em spec.md).

---

## Decisões de Implementação

### Segurança de senha e sessão

- Hash de senha: bcrypt via `passlib`.
- Sessão: cookie httpOnly com token opaco (`secrets.token_urlsafe(32)`); servidor guarda **SHA-256 do token** (nunca o token puro) + `user_id` + `expires_at` na collection `sessions`, com índice TTL em `expires_at` para expiração automática.

### Unicidade de cadastro

- `username` E `email` são únicos; conflito responde `409` indicando qual campo colidiu.

### Autorização de tarefas públicas

- Qualquer usuário autenticado pode editar/excluir tarefas `public` (modelo colaborativo), não só quem criou.
- Tarefas `personal` só podem ser editadas/excluídas pelo dono (`403` para os demais).

### Dados existentes

- Tarefas hoje no MongoDB não têm `owner_id`/`visibility` — serão apagadas (decisão do usuário) antes de ativar a feature.

### Tela inicial

- Bloqueia tudo até login: sem modo visitante/read-only público.

### Testes

- Usuário pediu testes automatizados em **backend (pytest) e frontend (Vitest + RTL)** — upgrade em relação ao estado atual do projeto (que não tinha nenhuma suíte).

### Discricionariedade do Agente

- Duração exata da sessão (24h fixa, sem sliding).
- Tamanho mínimo de senha (8 chars) e formato de username (3-30 `[a-zA-Z0-9_]`).
- Ausência de `react-router` — alternância de tela via estado local em `App.jsx`, consistente com o estilo de componente único já usado no projeto.

---

## Referências Específicas

Nenhuma referência visual/produto específica mencionada — abordagem padrão de login/registro simples (dois formulários, sem redesign visual do restante da UI).

---

## Ideias Adiadas

- Reset de senha / "esqueci minha senha"
- Rate limiting / proteção brute-force no login
- Papéis/permissões (admin, moderador)
- Edição de perfil (trocar senha/email)
- Grupos de compartilhamento seletivo (além do binário pessoal/público)

Todas capturadas em `spec.md` → Out of Scope; não perdidas, apenas fora do escopo desta feature.

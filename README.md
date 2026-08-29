# Central de novos projetos

Este diretório reúne um agente do VS Code e documentos para transformar uma ideia em um projeto executável.

## Estrutura

```text
Projetos/
├── README.md
├── .github/
│   └── agents/
│       └── iniciar-projeto.agent.md
├── docs/
│   ├── checklist-novo-projeto.md
│   └── guia-inicio-projeto.md
└── templates/
    └── README.md
```

## Como começar

1. Abra `c:\Projetos` no VS Code.
2. Selecione o agente **Iniciar Projeto** no seletor de agentes.
3. Informe a ideia do projeto, por exemplo: `Quero criar uma API para controlar minhas tarefas`.
4. Responda às perguntas do agente sobre objetivo, usuários, plataforma, dados e restrições.
5. Use o [guia de início](docs/guia-inicio-projeto.md) para revisar as decisões.
6. Copie o [checklist](docs/checklist-novo-projeto.md) para a pasta do projeto e acompanhe a execução.

## Regra simples

Comece com o menor projeto que prove o valor principal. Escolha a tecnologia depois de esclarecer o problema, o primeiro fluxo de usuário e a forma de validar o resultado.

## Arquivos principais

- [Agente Iniciar Projeto](.github/agents/iniciar-projeto.agent.md): orienta a descoberta, o planejamento e a criação do primeiro incremento.
- [Guia de início](docs/guia-inicio-projeto.md): explica o processo em etapas.
- [Checklist](docs/checklist-novo-projeto.md): lista operacional para não esquecer decisões básicas.
- [Template de projeto](templates/README.md): conteúdo mínimo recomendado para a pasta de cada projeto.

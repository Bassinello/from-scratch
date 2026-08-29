# Guia para iniciar um novo projeto

Este guia serve para qualquer projeto de software, mesmo quando a linguagem ainda não foi escolhida.

## 1. Escreva o problema

Complete esta frase:

> Para **[público]**, que precisa **[necessidade]**, vamos criar **[produto ou serviço]**, para que **[resultado observável]**.

Exemplo:

> Para estudantes que perdem prazos, vamos criar uma aplicação de tarefas, para que consigam ver e concluir suas entregas da semana.

Evite começar por uma tecnologia. Tecnologia é uma decisão de implementação; o problema define o que precisa ser validado.

## 2. Defina o primeiro fluxo

Descreva o caminho principal em três a sete passos. Exemplo:

1. Usuário abre a aplicação.
2. Cria uma tarefa com título e prazo.
3. Consulta as tarefas pendentes.
4. Marca uma tarefa como concluída.

Esse fluxo vira a referência do MVP.

## 3. Escolha o MVP

MVP é o menor conjunto de funcionalidades que permite aprender algo real. Separe as ideias assim:

| Categoria | Pergunta | Exemplo |
| --- | --- | --- |
| Essencial | Sem isso o fluxo principal funciona? | Criar tarefa |
| Importante | Melhora o uso, mas pode esperar? | Filtrar por prazo |
| Futuro | É uma hipótese ainda não validada? | Recomendações automáticas |

Comece com três a cinco entregas essenciais. Para cada uma, escreva um critério de aceite verificável.

Exemplo: `Dado um título válido, ao salvar a tarefa, ela aparece na lista de pendências.`

## 4. Escolha a stack

Considere nesta ordem:

1. Conhecimento da equipe.
2. Requisitos do produto.
3. Bibliotecas maduras e documentação disponível.
4. Custo e simplicidade de execução.
5. Necessidade de escala, segurança e observabilidade.

Para um projeto pessoal ou protótipo, prefira uma stack que possa ser executada localmente com poucos comandos. Para um sistema de produção, registre também autenticação, persistência, backups, logs, monitoramento e estratégia de deploy.

## 5. Crie a estrutura mínima

Uma base genérica pode conter:

```text
meu-projeto/
├── README.md
├── .gitignore
├── docs/
│   ├── requisitos.md
│   └── decisoes.md
├── src/
├── tests/
└── .env.example
```

Adapte os nomes ao ecossistema escolhido. Não crie pastas vazias apenas por convenção.

## 6. Documente a execução

O `README.md` do projeto deve responder rapidamente:

- O que o projeto faz.
- Quais são os pré-requisitos.
- Como instalar dependências.
- Como configurar variáveis de ambiente.
- Como executar em desenvolvimento.
- Como rodar testes e verificações.
- Onde encontrar a documentação funcional.

Use comandos que possam ser copiados e executados. Se houver mais de um sistema operacional, registre as diferenças relevantes.

## 7. Faça uma primeira verificação

Antes de adicionar funcionalidades, confirme que a base funciona:

- O projeto instala sem erros.
- A aplicação inicia ou o comando principal executa.
- Um teste mínimo passa.
- O lint, formatador ou compilador está configurado quando fizer sentido.
- Segredos não estão no repositório.

Essa verificação reduz o risco de construir funcionalidades sobre uma base quebrada.

## 8. Trabalhe em incrementos

Para cada incremento, registre:

- Objetivo.
- Critérios de aceite.
- Arquivos ou módulos afetados.
- Como validar.
- O que ficou deliberadamente fora.

Faça commits pequenos e com mensagens que expliquem a mudança. Revise o MVP depois de cada validação; requisitos novos devem entrar como decisão explícita, não como acúmulo silencioso.

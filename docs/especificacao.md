# Radar da Mooca

## Capa — Global Solution 2026.2 · Engenharia de Software

**Tema:** Urban Risk Intelligence Platform · CitizenTech  
**Equipe:** Lucas Zolla Assis — RM 557952; Lucas Baraldi Rodrigues — RM 555407; Vitor Pantarotto de Brito — RM 554961.  
**Recorte:** bairro da Mooca, São Paulo/SP.  
**Prazo informado pela equipe:** 19/11/2026. **Meta interna:** 16/11/2026.  
**Repositório:** https://github.com/VitorPDB/GS-eng-software  
**Protótipo publicado:** PENDENTE — inserir endereço público após publicação e teste anônimo.  
**Vídeo de demonstração:** PENDENTE — inserir endereço após gravação, com acesso público ou não listado.

Documento técnico do protótipo acadêmico. Todos os eventos, sensores, bases e registros demonstrados são fictícios. A aplicação não é um serviço operacional de emergência. Os nomes de fontes devem indicar simulação e não sugerir integração com órgãos reais.

## 1. Problema, público e proposta

Informações sobre alagamentos, calor intenso e interrupções de serviços podem aparecer em canais distintos, sem indicação clara de atualização, origem ou confirmação. Para um morador, isso dificulta identificar o que acontece perto de casa. Para um agente local, dificulta distinguir uma ocorrência inicial de um evento validado e priorizar o acompanhamento.

O Radar da Mooca organiza ocorrências em uma visão geral por região e tipo, oferece alertas e notificações internas e permite acompanhar a origem dos dados. A demonstração cobre três tipos de fonte: sensor simulado, base pública simulada e registro comunitário fictício. O cenário principal é um alagamento; calor e interrupção de serviços demonstram a abrangência do tema com o mesmo modelo de evento.

O valor central é tornar explícitas duas perguntas distintas: **qual é a gravidade do evento?** e **quanta evidência sustenta o registro?** Risco e confiança aparecem separados. A confiança é uma pontuação explicável das evidências do protótipo, sem interpretação de probabilidade estatística.

### Personas fictícias

| Persona | Contexto e objetivo | Necessidade atendida |
|---|---|---|
| Ana, moradora da Mooca | Consulta o bairro antes de sair; usa celular e precisa de leitura rápida | Ver risco, localização aproximada, horário e situação do alerta sem depender apenas de cores |
| Rafael, agente local | Confere relatos e acompanha evolução de eventos | Inspecionar evidências, justificar confirmação ou descarte e registrar mudanças de estado |
| Joana, operadora de serviço | Acompanha uma interrupção fictícia de abastecimento | Identificar fonte, atualização e histórico em uma visão comum do evento |

As personas não representam pessoas entrevistadas. São hipóteses de público para orientar o projeto acadêmico.

## 2. Escopo e limites

Será entregue um protótipo web estático funcional em HTML, CSS e JavaScript ES Modules, com oito telas distintas e fluxos navegáveis. O processamento ocorre no navegador. O repositório local persiste o estado em `localStorage`; se o armazenamento estiver indisponível, mantém a sessão em memória e informa a limitação.

Não há backend, autenticação real, consulta a sensores reais, consumo de bases públicas reais, geolocalização automática, envio de SMS ou e-mail. A troca entre morador e agente é uma ferramenta demonstrativa, sem controle real de acesso. As notificações são registros internos da aplicação. O painel de visão geral atende ao briefing sem exigir um mapa geográfico interativo.

### Oito telas

| ID | Tela | Conteúdo e ação principal |
|---|---|---|
| T01 | Painel | Visão geral, indicadores, ocorrências por tipo e acesso aos alertas |
| T02 | Alertas | Lista com risco e estado, permitindo abrir o evento selecionado |
| T03 | Detalhe do evento | Evidências resumidas, risco, confiança, justificativa e ações compatíveis com o estado |
| T04 | Notificações | Alertas publicados no protótipo, leitura e acesso ao evento associado |
| T05 | Registro comunitário | Formulário de ocorrência com validação e confirmação na própria tela |
| T06 | Origem e confiança | Fontes fictícias, tipo, horário, atualidade e composição da pontuação |
| T07 | Validação do agente | Conferência, justificativa, confirmação ou descarte e ações de acompanhamento |
| T08 | Histórico | Linha do tempo de estados, motivos e alterações do evento |

A confirmação do formulário é um estado da T05 e não é contada como uma nona tela. Um detalhe aberto para outro evento continua sendo a T03.

## 3. Regras de negócio

### RB01 — Relógio e dados da demonstração

O relógio de referência é **06/11/2026 às 14h30, America/Sao_Paulo**, equivalente a `2026-11-06T14:30:00-03:00`. Os horários dos dados são interpretados em relação a essa referência, para tornar a demonstração reproduzível. Esse relógio fixo deve ser identificado na interface. Atualidade demonstrada não significa atualização real da cidade.

### RB02 — Classificação do risco

Cada evento possui impacto e urgência, ambos inteiros de 1 a 3. O impacto representa a extensão ou intensidade potencial do efeito; a urgência representa quão imediata é a necessidade de acompanhamento no cenário fictício. O registro inicial pode usar a avaliação do relator, sujeita à conferência pelo agente.

`pontuação de risco = impacto + urgência`

| Soma | Classificação |
|---|---|
| 2 | Baixo |
| 3 ou 4 | Moderado |
| 5 ou 6 | Alto |

Valores ausentes, fracionários ou fora de 1 a 3 devem ser rejeitados. Esta regra é uma convenção acadêmica explicável; não é um modelo meteorológico ou protocolo oficial de Defesa Civil.

### RB03 — Atualidade das fontes

Uma fonte é fresca quando seu horário é válido e sua idade está entre 0 e 30 minutos, inclusive, em relação ao relógio da demonstração. Horários futuros ou inválidos não contam como evidência fresca. Duplicar registros do mesmo tipo de fonte não cria diversidade: os tipos são sensor, base pública e comunidade.

### RB04 — Pontuação de confiança

Somar, uma única vez por critério:

| Evidência | Pontos |
|---|---:|
| Existe pelo menos uma fonte fresca | 30 |
| Existem pelo menos dois tipos distintos de fonte fresca | 30 |
| Existe validação do agente registrada como `verified = true` | 40 |

Confiança **alta**: 80 a 100; **média**: 50 a 79; **baixa**: abaixo de 50. A tela deve apresentar os critérios atendidos e os horários que justificam a classificação. Uma única fonte comunitária fresca e sem validação resulta em 30 pontos e confiança baixa. Uma fonte fresca com validação resulta em 70 pontos e confiança média. Dois tipos frescos com validação resultam em 100 pontos e confiança alta. Com esta fórmula discreta, nem todos os inteiros de 0 a 100 são resultados possíveis.

### RB05 — Ciclo de vida

Um registro comunitário nasce em `reportado`. Transições permitidas:

| Origem | Destino | Condição ou ação |
|---|---|---|
| `reportado` | `em_validacao` | Agente inicia conferência |
| `reportado` | `descartado` | Descarte com motivo obrigatório |
| `em_validacao` | `confirmado` | Motivo preenchido e pelo menos uma fonte fresca; registrar `verified = true` |
| `em_validacao` | `descartado` | Descarte com motivo obrigatório |
| `confirmado` | `alerta_emitido` | Aplicar RB06 |
| `confirmado` | `em_monitoramento` | Risco baixo; acompanhamento sem publicação de alerta |
| `alerta_emitido` | `em_monitoramento` | Iniciar acompanhamento do alerta publicado |
| `em_monitoramento` | `encerrado` | Registrar encerramento com justificativa |

`encerrado` e `descartado` são estados terminais neste recorte. Transições não previstas devem ser recusadas, sem alterar o estado. Os nomes legíveis da interface podem usar espaços e acentos, preservando os mesmos estados no modelo e nos diagramas.

### RB06 — Publicação e notificação

A publicação requer simultaneamente: estado `confirmado`, confiança de pelo menos 50 pontos, pelo menos uma fonte fresca e risco moderado ou alto. Ao publicar, o evento passa para `alerta_emitido` e gera uma notificação interna associada à publicação. Tentativas repetidas sobre a mesma publicação não podem duplicar notificações. A interface informa o bloqueio e o critério faltante quando uma condição não é satisfeita.

### RB07 — Prioridade e transparência

Alertas de risco alto precedem os moderados e os baixos na apresentação prioritária. Em empate, usar o registro mais recente; em novo empate, o identificador fornece ordem estável. A lista mostra risco e confiança separadamente. Uma pontuação de risco alta não transforma um relato sem confirmação em fato validado.

### RB08 — Privacidade e linguagem

O protótipo utiliza apenas dados fictícios, localização aproximada e descrição da ocorrência. Não solicita nome do relator, documento, telefone ou endereço residencial completo. Orientar o usuário a não inserir dados pessoais no texto livre. O histórico não expõe a identidade de um relator. Essas decisões são diretrizes de minimização e proteção de dados inspiradas na LGPD; não constituem certificação ou garantia de conformidade jurídica.

## 4. Requisitos funcionais

Prioridades: **P1** essencial à entrega; **P2** complemento de qualidade. Os critérios abaixo são condições de aceite planejadas.

| ID | Descrição | Prioridade | Critério de aceite |
|---|---|---|---|
| RF01 | Exibir painel de acompanhamento dos três tipos de risco | P1 | T01 apresenta alagamento, calor e interrupção de serviço com acesso aos eventos |
| RF02 | Listar e priorizar alertas | P1 | T02 exibe risco, confiança e estado, aplicando RB07 e permitindo abrir T03 |
| RF03 | Exibir o detalhe de um evento | P1 | T03 apresenta tipo, região aproximada, horários, estado, risco e confiança |
| RF04 | Receber registro comunitário fictício | P1 | T05 exige campos válidos, cria identificador e estado `reportado`, com confirmação inline |
| RF05 | Representar dados de três tipos de fonte | P1 | O conjunto demonstrativo inclui sensor, base pública e comunidade, todos identificados como simulados |
| RF06 | Calcular e explicar risco e confiança | P1 | Valores obedecem RB02–RB04 e os critérios podem ser inspecionados em T03/T06 |
| RF07 | Permitir validação e descarte pelo perfil demonstrativo de agente | P1 | T07 exige motivos e aplica as condições de RB05, com mensagem nos bloqueios |
| RF08 | Publicar alerta após validação | P1 | Somente eventos elegíveis pela RB06 transitam para `alerta_emitido` |
| RF09 | Manter central de notificações internas | P1 | T04 apresenta a notificação vinculada ao evento; publicação repetida não gera duplicata |
| RF10 | Acompanhar e encerrar o evento | P1 | RB05 rege monitoramento e encerramento, com motivo e estado atualizado |
| RF11 | Exibir histórico de alterações | P1 | T08 apresenta sequência temporal de estados e justificativas do evento selecionado |
| RF12 | Preservar o estado local e oferecer reinício da demonstração | P2 | Reabertura mantém o estado quando houver armazenamento; reinício restaura os cenários fictícios e falha de armazenamento usa memória com aviso |

## 5. Requisitos não funcionais

Classificação orientada pela **ISO/IEC 25010:2023**. A edição 2023 define nove características de qualidade de produto; os oito requisitos abaixo selecionam as pertinentes ao recorte, sem pretender cobrir toda a norma. “Capacidade de interação” é empregada para o objetivo de usabilidade; “flexibilidade” organiza a meta de escalabilidade. Fonte de referência: [página oficial ISO/IEC 25010:2023](https://www.iso.org/standard/78176.html).

| ID | Característica | Requisito mensurável e condição de verificação | Alcance |
|---|---|---|---|
| RNF01 | Eficiência de desempenho | Após receber um registro ou executar uma transição local, atualizar a interface em até 1 segundo em navegador desktop atual, com até 100 eventos fictícios; medir 20 ações e registrar tempos | Meta verificável do protótipo; não medida neste documento |
| RNF02 | Confiabilidade — disponibilidade | Em uma implantação futura, alcançar disponibilidade mensal de 99,5%, medida por monitor externo; no protótipo, uma falha de `localStorage` não deve impedir navegar nem registrar dados na sessão em memória | Disponibilidade de produção é meta futura; contingência local é verificável |
| RNF03 | Flexibilidade — escalabilidade | Em produção futura, suportar 1.000 eventos/minuto por 15 minutos, com processamento p95 de até 5 segundos, usando processamento desacoplado e ampliação de capacidade | Meta arquitetural futura; não comprovada pelo site estático |
| RNF04 | Capacidade de interação | Nas oito telas, permitir alcançar controles por teclado, mostrar foco visível e usar texto/ícone além da cor para risco e confiança; validar a 360 px e 1280 px sem rolagem horizontal da página | Inspeção e teste de navegação planejados; não afirmar certificação de acessibilidade |
| RNF05 | Segurança | Formulário sem campos de identificação pessoal; localização aproximada; toda entrada livre renderizada como texto, sem execução de HTML; verificar com uma carga de teste contendo marcação HTML | Diretriz de minimização/LGPD e teste local, sem autenticação real |
| RNF06 | Confiabilidade | Para transição inválida, fonte desatualizada, campos inválidos e falha de armazenamento, preservar consistência e exibir mensagem; executar ao menos um cenário de cada condição | Critério de robustez do protótipo |
| RNF07 | Adequação funcional | Cem por cento das publicações devem respeitar RB06; cada publicação válida gera exatamente uma notificação; validar limites de risco, confiança e frescor | Testes de regras e integração planejados |
| RNF08 | Manutenibilidade | Regras de risco, confiança e transições devem estar no domínio, sem importar DOM ou armazenamento; casos de uso recebem repositório por injeção; verificar dependências e executar regras isoladamente | Inspeção de código e testes planejados |

As metas numéricas são propostas de projeto e precisam de evidência de medição antes de serem declaradas atendidas. O RNF01 trata do tempo de atualização **local**; o RNF03 descreve uma possível evolução de ingestão em produção. O relógio fixo da demonstração não mede latência de fontes urbanas reais.

## 6. Arquitetura prática e evolução

### Implementação acadêmica

| Camada | Responsabilidade | Elementos e limite |
|---|---|---|
| Apresentação | Navegação, formulários, renderização e feedback | `app.js` atua como controlador e reúne as views; traduz ações para casos de uso |
| Aplicação | Orquestrar registro, validação, publicação e acompanhamento | Módulo `platform` coordena domínio e repositório injetado; gera notificação interna na publicação |
| Domínio | Expressar regras e invariantes | Módulo `rules`: risco, confiança, frescor e transições; não conhece DOM nem `localStorage` |
| Infraestrutura/dados | Ler e escrever estado da demonstração | Repositório com `localStorage`, contingência em memória e dados iniciais simulados (`seed`) |
| Fontes externas representadas | Ilustrar entradas previstas no tema | Sensor simulado, base pública simulada e comunidade fictícia; não existem conectores reais |

O ponto de composição cria o repositório e o injeta na aplicação. O domínio não importa a infraestrutura. O repositório abstrai a persistência necessária ao protótipo, evitando adicionar servidor ou banco apenas para demonstrar navegação.

A organização usa separação em camadas e responsabilidades próximas de MVC: as views apresentam, o controlador recebe ações e o modelo é expresso por domínio e aplicação. A injeção do repositório cria um limite compatível com princípios de Clean/Hexagonal, sem afirmar que o protótipo implementa integralmente esses estilos. Os conceitos são aplicados como decisões do projeto; não se alega reprodução literal de material de aula não consultado.

As mudanças de estado representam eventos de negócio no modelo. A notificação interna é produzida por um caso de uso local; **não existe broker, fila distribuída ou arquitetura de microsserviços** nesta entrega.

### Proteção de dados e notificações

A apresentação limita os campos e informa que os dados são fictícios. A aplicação valida as operações. O domínio impõe as condições de publicação. O repositório mantém apenas o estado local da demonstração. A troca de perfil não protege dados nem concede autorização de produção; é um recurso para percorrer os dois papéis na apresentação acadêmica.

### Evolução futura, fora da entrega

Uma versão operacional exigiria API de ingestão, autenticação e autorização reais, banco de dados, monitoramento, política de retenção, gestão de incidentes e validação jurídica e técnica. Adaptadores poderiam receber fontes autorizadas; uma fila e consumidores poderiam apoiar a meta de ingestão do RNF03. Um serviço de notificações poderia tratar canais externos, consentimentos e entregas. Essas possibilidades não são funcionalidades concluídas ou compromissos do protótipo.

## 7. Fluxos e exceções

### Fluxo principal da demonstração

1. Morador consulta T01/T02 e identifica os riscos fictícios do bairro.
2. Registra um alagamento em T05; recebe protocolo inline e estado `reportado`.
3. Acessa T03/T06 para conferir fonte comunitária, horário e confiança inicial baixa.
4. Troca para o perfil demonstrativo de agente e abre T07.
5. Inicia validação, confere fonte fresca e informa motivo; confirma o evento.
6. Consulta o cálculo atualizado de risco e confiança. Sendo elegível, publica o alerta.
7. T04 recebe uma notificação interna vinculada ao evento.
8. Agente acompanha e encerra o evento; T08 registra o percurso e as justificativas.

### Caminhos alternativos

| Condição | Resultado esperado |
|---|---|
| Campo obrigatório vazio ou impacto/urgência inválido | Mostrar mensagem junto ao formulário; não criar registro parcial |
| Fonte desatualizada ou de horário inválido | Não contar como fresca; mostrar a condição; bloquear confirmação/publicação que dependa dela |
| Relato único recém-enviado | Mostrar confiança baixa e estado reportado; não publicar automaticamente |
| Tentativa de confirmar sem motivo | Manter estado e solicitar justificativa |
| Evento confirmado de risco baixo | Permitir monitoramento, sem notificação de publicação |
| Descarte | Exigir motivo; terminar ciclo sem produzir alerta |
| Transição não permitida | Informar o bloqueio; não alterar evento ou histórico indevidamente |
| Publicação repetida | Não criar segunda notificação para a mesma publicação |
| Armazenamento indisponível | Usar memória com aviso de que os dados da sessão podem se perder ao recarregar |

## 8. Rastreabilidade e verificação planejada

Os identificadores de cenários abaixo descrevem **verificações planejadas**. Esta especificação não registra execução ou aprovação de testes. Evidências e resultados devem ser acrescentados após rodar a versão final.

| Teste | Verificação planejada |
|---|---|
| AT01 | Abrir painel/lista e navegar para um evento de cada tipo de risco |
| AT02 | Conferir campos de detalhe, origem e horários em fontes dos três tipos |
| AT03 | Enviar registro válido; conferir protocolo e estado; rejeitar formulário inválido |
| AT04 | Testar somas de risco 2, 3, 4, 5 e 6 e rejeitar valores fora do intervalo |
| AT05 | Testar frescor em 0, 30 e 31 minutos; horários futuros e inválidos |
| AT06 | Conferir confiança 30, 60, 70 e 100, sem pontuar repetidamente o mesmo critério |
| AT07 | Percorrer validação/confirmação e bloquear ausência de motivo ou fonte fresca |
| AT08 | Publicar evento elegível, bloquear inelegível e conferir notificação única |
| AT09 | Percorrer monitoramento/encerramento e descarte; rejeitar transição inválida |
| AT10 | Conferir histórico, persistência, reinício e contingência sem armazenamento |
| AT11 | Medir atualização local segundo RNF01 com conjunto de 100 eventos |
| UX01 | Percorrer as oito telas por teclado e conferir foco, rótulos e texto além da cor |
| UX02 | Revisar navegação e layout em 360 px e 1280 px |
| SEC01 | Conferir minimização de campos e renderização de HTML como texto |
| ARQ01 | Inspecionar dependências e executar regras sem DOM/armazenamento |

### Matriz requisito ↔ tela ↔ componente ↔ teste

| Requisito | Tela | Componente principal | Teste planejado |
|---|---|---|---|
| RF01 | T01 | Apresentação / plataforma | AT01, UX02 |
| RF02 | T02 | Apresentação / regras de prioridade | AT01, AT04 |
| RF03 | T03 | Apresentação / plataforma | AT02 |
| RF04 | T05 | Apresentação / caso de uso de registro | AT03, SEC01 |
| RF05 | T01, T03, T06 | Seed / repositório / plataforma | AT02 |
| RF06 | T03, T06 | Domínio `rules` | AT04, AT05, AT06 |
| RF07 | T07 | Plataforma / domínio | AT07, AT09 |
| RF08 | T03, T07 | Caso de uso de publicação / domínio | AT08 |
| RF09 | T04 | Plataforma / repositório | AT08 |
| RF10 | T03, T07 | Plataforma / domínio | AT09 |
| RF11 | T08 | Plataforma / repositório | AT09, AT10 |
| RF12 | T01–T08 | Repositório / seed | AT10 |
| RNF01 | T01–T08 | Apresentação / plataforma | AT11 |
| RNF02 | T01–T08 | Repositório; hospedagem futura | AT10; monitoramento futuro pendente |
| RNF03 | Sem tela dedicada | API/fila/consumidores futuros | Teste de carga futuro, fora do protótipo |
| RNF04 | T01–T08 | Apresentação / estilos | UX01, UX02 |
| RNF05 | T03, T05, T06, T08 | Apresentação / plataforma | SEC01 |
| RNF06 | T03, T05, T07 | Plataforma / domínio / repositório | AT03, AT05, AT07, AT09, AT10 |
| RNF07 | T03, T04, T07 | Domínio / plataforma | AT04–AT08 |
| RNF08 | Sem tela dedicada | Limites de módulos | ARQ01 |

### Coerência dos diagramas

O diagrama de sequência deve representar a fonte simulada ou o morador, a apresentação, a aplicação, as regras de domínio e o repositório. Deve mostrar recebimento, validação, classificação, persistência e publicação com notificação interna; condições inválidas precisam ser identificadas. Não incluir SMS, integração real ou fila como se estivessem implementados.

O diagrama de estados deve reproduzir RB05, incluindo guardas de confirmação e publicação, o caminho de risco baixo e o descarte com motivo. A visão de arquitetura deve distinguir as quatro camadas implementadas e as fontes externas apenas representadas. Os diagramas finais serão incorporados ao PDF único; este arquivo não substitui sua entrega visual.

## 9. Backlog e organização da entrega

| Ordem | Entrega | Critério de conclusão |
|---|---|---|
| 1 | Regras e cenário principal | Risco/confiança/transições coerentes e cenário reproduzível |
| 2 | Oito telas e fluxo completo | Navegação morador→agente→notificação→histórico, com mensagens de exceção |
| 3 | Verificação e ajustes | Executar cenários pertinentes, corrigir falhas e registrar evidências |
| 4 | Documentação e diagramas | Revisão cruzada dos requisitos, componentes, estados e telas |
| 5 | Publicação, PDF e vídeo | Links acessíveis em janela anônima, PDF único e vídeo até três minutos |

### Cronograma de referência

| Período de novembro de 2026 | Objetivo |
|---|---|
| 06–08 | Fechar recorte, regras, arquitetura e oito telas |
| 09–11 | Concluir fluxo principal e persistência local; preparar diagramas |
| 12–13 | Executar verificações, ajustar acessibilidade e revisar rastreabilidade |
| 14–15 | Consolidar PDF, publicar protótipo e gravar vídeo |
| 16 | Meta interna: pacote revisado e links testados |
| 17–18 | Reserva para correções finais |
| 19 | Prazo informado: envio por um integrante no Teams, em nome do grupo |

As datas são planejamento, não registro de tarefas já concluídas. A divisão de responsáveis deve ser acordada pelo trio. O calendário oficial da instituição deve ser conferido antes do envio.

## 10. Composição do pacote final

O PDF único deve começar com os três nomes completos, RMs e links do protótipo, repositório e vídeo. Deve incluir problema, público, personas, 12 RF, 8 RNF, regras, diagrama de sequência, diagrama de estados e visão de arquitetura em camadas. Os links pendentes não devem permanecer como pendências na versão enviada.

O repositório precisa conter instruções de execução no README. O vídeo deve apresentar problema, solução e navegação pelo fluxo principal em até três minutos. O protótipo e o vídeo precisam ser acessíveis a quem avaliar, com teste em janela anônima. O checklist e o roteiro desta pasta apoiam a finalização.

O grupo deve revisar e compreender tudo o que entregar, inclusive material elaborado com apoio de IA. As exigências acadêmicas foram extraídas das imagens fornecidas; as decisões de escopo e os critérios numéricos de risco/confiança são propostas deste projeto, e não regras atribuídas ao enunciado.

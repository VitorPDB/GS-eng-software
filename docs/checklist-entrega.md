# Radar da Mooca — checklist de entrega

Prazo informado: **19/11/2026**. Meta interna: **16/11/2026**. Conferir calendário oficial antes do envio. Uma caixa vazia significa que a conferência ainda precisa ser registrada; não implica que o artefato esteja ausente.

## Identificação e links

- [x] Primeira página do PDF com Lucas Zolla Assis — RM 557952; Lucas Baraldi Rodrigues — RM 555407; Vitor Pantarotto de Brito — RM 554961.
- [x] Repositório acessível: https://github.com/VitorPDB/GS-eng-software.
- [x] Link público do protótipo publicado: https://vitorpdb.github.io/GS-eng-software/.
- [ ] Link do vídeo público ou não listado — **PENDENTE**.
- [ ] Todos os links da capa testados em janela anônima, sem depender da sessão do autor.

## Documento único em PDF

- [x] Problema, público-alvo e personas fictícias descritos.
- [x] Doze requisitos funcionais com identificador, descrição, prioridade e aceite.
- [x] Oito RNF mensuráveis classificados pela ISO/IEC 25010:2023.
- [x] RNF cobrem atualização, disponibilidade, escalabilidade, interação/usabilidade e segurança/LGPD.
- [x] Metas futuras de produção claramente distinguidas do que o protótipo comprova.
- [x] Regras de risco, confiança, fontes frescas, publicação e prioridade descritas.
- [x] Diagrama de sequência UML com recebimento, validação, classificação e notificação.
- [x] Diagrama de estados UML com guardas, descarte, monitoramento e encerramento.
- [x] Visão de arquitetura em camadas com fontes simuladas, notificação e proteção de dados posicionadas.
- [x] Matriz requisito ↔ tela ↔ componente ↔ cenário revisada contra o código e os diagramas.
- [x] PDF renderizado e revisado visualmente, sem cortes ou texto ilegível; links definidos na capa. Conferência final dos links após inserir o vídeo permanece abaixo.
- [x] Documentação completa em um único PDF gerado: `radar-da-mooca-documentacao.pdf` (versão para revisão; vídeo pendente).

## Protótipo

- [x] T01 — Painel de acompanhamento.
- [x] T02 — Lista de alertas.
- [x] T03 — Detalhe do evento.
- [x] T04 — Central de notificações internas.
- [x] T05 — Registro comunitário, com confirmação inline.
- [x] T06 — Origem e confiança dos dados.
- [x] T07 — Validação pelo agente.
- [x] T08 — Histórico.
- [x] Oito telas distintas; confirmação inline não contada como tela extra.
- [x] Dados e fontes identificados como fictícios; relógio fixo indicado.
- [x] Sensor, base pública e comunidade representados sem sugerir integrações reais.
- [x] Fluxo completo registro→validação→confirmação→publicação→notificação→monitoramento→encerramento.
- [x] Caminho de descarte com motivo demonstrável.
- [x] Risco e confiança separados, com critérios, origem e horário visíveis.
- [x] Perfis identificados como demonstração, sem alegação de autenticação real.
- [x] Nenhum envio real de SMS/e-mail ou captura desnecessária de dados pessoais.
- [x] Repositório com README e instruções suficientes para executar o protótipo.

## Verificação e evidências

Resultados da versão local de 06/11/2026 registrados em `verificacao-qa.md`: 15 testes aprovados, zero falhas, jornada completa no navegador e oito telas verificadas a 360/1280 px. Os itens marcados correspondem às evidências disponíveis. Os cenários mais amplos ainda não inteiramente cobertos permanecem abertos.

- [x] AT01–AT03: navegação, fontes e registro válido/inválido.
- [x] AT04: completar todos os limites 2/3/4/5/6 e entradas fora de 1 a 3; há cobertura parcial de risco e validação nos testes atuais.
- [x] AT05: completar matriz exata de 0/30/31 minutos e horário inválido; limite de 30 minutos, obsolescência e horário futuro já exercitados.
- [x] AT06: confiança, diversidade de fontes e ausência de pontuação duplicada.
- [x] AT07: confirmação bloqueada sem motivo ou fonte fresca.
- [x] AT08: publicação condicionada e notificação única.
- [x] AT09: transições válidas, inválidas, descarte e encerramento.
- [x] AT10: histórico, persistência, reinício e contingência em memória.
- [ ] AT11: tempo de atualização local medido nas condições do RNF01.
- [x] UX02: oito telas a 360/1280 px, sem rolagem horizontal da página nas combinações verificadas.
- [ ] UX01: auditoria completa de teclado, foco, contraste e leitura por tecnologia assistiva; estilos e texto além da cor não substituem a auditoria.
- [ ] Testar tarefas com usuários reais.
- [x] SEC01: minimização de campos e entrada HTML renderizada como texto.
- [x] ARQ01: domínio independente de DOM/armazenamento e repositório injetado.
- [x] Sem apresentar RNF de produção como comprovados por testes locais.

## Vídeo e envio

- [ ] Roteiro ensaiado com fluxo reproduzível e dados restaurados.
- [ ] Vídeo apresenta problema, solução e navegação principal.
- [ ] Duração final até três minutos; áudio e interface legíveis.
- [ ] Vídeo reproduz em janela anônima.
- [ ] Grupo revisou e compreende texto, código, regras e diagramas, inclusive conteúdo apoiado por IA.
- [ ] Links finais substituem todas as marcações PENDENTE do PDF.
- [ ] Um integrante designado envia o PDF pelo Teams em nome do trio.
- [ ] Comprovante de envio conferido antes do prazo oficial.

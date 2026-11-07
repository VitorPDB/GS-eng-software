# Radar da Mooca — checklist de entrega

Prazo informado: **19/11/2026**. Meta interna: **16/11/2026**. Conferir calendário oficial antes do envio. Uma caixa vazia significa que a conferência ainda precisa ser registrada; não implica que o artefato esteja ausente.

## Identificação e links

- [ ] Primeira página do PDF com Lucas Zolla Assis — RM 557952; Lucas Baraldi Rodrigues — RM 555407; Vitor Pantarotto de Brito — RM 554961.
- [ ] Repositório acessível: https://github.com/VitorPDB/GS-eng-software.
- [ ] Link público do protótipo publicado — **PENDENTE**.
- [ ] Link do vídeo público ou não listado — **PENDENTE**.
- [ ] Todos os links da capa testados em janela anônima, sem depender da sessão do autor.

## Documento único em PDF

- [ ] Problema, público-alvo e personas fictícias descritos.
- [ ] Doze requisitos funcionais com identificador, descrição, prioridade e aceite.
- [ ] Oito RNF mensuráveis classificados pela ISO/IEC 25010:2023.
- [ ] RNF cobrem atualização, disponibilidade, escalabilidade, interação/usabilidade e segurança/LGPD.
- [ ] Metas futuras de produção claramente distinguidas do que o protótipo comprova.
- [ ] Regras de risco, confiança, fontes frescas, publicação e prioridade descritas.
- [ ] Diagrama de sequência UML com recebimento, validação, classificação e notificação.
- [ ] Diagrama de estados UML com guardas, descarte, monitoramento e encerramento.
- [ ] Visão de arquitetura em camadas com fontes simuladas, notificação e proteção de dados posicionadas.
- [ ] Matriz requisito ↔ tela ↔ componente ↔ cenário revisada contra o código e os diagramas.
- [ ] PDF renderizado e revisado visualmente, sem cortes, texto ilegível ou links quebrados.
- [ ] Arquivo final contém a documentação completa em um único PDF — **geração do PDF pendente nesta etapa**.

## Protótipo

- [ ] T01 — Painel de acompanhamento.
- [ ] T02 — Lista de alertas.
- [ ] T03 — Detalhe do evento.
- [ ] T04 — Central de notificações internas.
- [ ] T05 — Registro comunitário, com confirmação inline.
- [ ] T06 — Origem e confiança dos dados.
- [ ] T07 — Validação pelo agente.
- [ ] T08 — Histórico.
- [ ] Oito telas distintas; confirmação inline não contada como tela extra.
- [ ] Dados e fontes identificados como fictícios; relógio fixo indicado.
- [ ] Sensor, base pública e comunidade representados sem sugerir integrações reais.
- [ ] Fluxo completo registro→validação→confirmação→publicação→notificação→monitoramento→encerramento.
- [ ] Caminho de descarte com motivo demonstrável.
- [ ] Risco e confiança separados, com critérios, origem e horário visíveis.
- [ ] Perfis identificados como demonstração, sem alegação de autenticação real.
- [ ] Nenhum envio real de SMS/e-mail ou captura desnecessária de dados pessoais.
- [ ] Repositório com README e instruções suficientes para executar o protótipo.

## Verificação e evidências

As verificações abaixo são **planejadas**. Registrar versão, data, resultado e evidência antes de marcá-las.

- [ ] AT01–AT03: navegação, fontes e registro válido/inválido.
- [ ] AT04: limites do risco e entradas fora de 1 a 3.
- [ ] AT05: frescor em 0, 30 e 31 minutos, horário futuro e inválido.
- [ ] AT06: confiança, diversidade de fontes e ausência de pontuação duplicada.
- [ ] AT07: confirmação bloqueada sem motivo ou fonte fresca.
- [ ] AT08: publicação condicionada e notificação única.
- [ ] AT09: transições válidas, inválidas, descarte e encerramento.
- [ ] AT10: histórico, persistência, reinício e contingência em memória.
- [ ] AT11: tempo de atualização local medido nas condições do RNF01.
- [ ] UX01–UX02: teclado, foco, texto além de cores e layout a 360/1280 px.
- [ ] SEC01: minimização de campos e entrada HTML renderizada como texto.
- [ ] ARQ01: domínio independente de DOM/armazenamento e repositório injetado.
- [ ] Sem apresentar RNF de produção como comprovados por testes locais.

## Vídeo e envio

- [ ] Roteiro ensaiado com fluxo reproduzível e dados restaurados.
- [ ] Vídeo apresenta problema, solução e navegação principal.
- [ ] Duração final até três minutos; áudio e interface legíveis.
- [ ] Vídeo reproduz em janela anônima.
- [ ] Grupo revisou e compreende texto, código, regras e diagramas, inclusive conteúdo apoiado por IA.
- [ ] Links finais substituem todas as marcações PENDENTE do PDF.
- [ ] Um integrante designado envia o PDF pelo Teams em nome do trio.
- [ ] Comprovante de envio conferido antes do prazo oficial.

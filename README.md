# Radar da Mooca

Protótipo acadêmico da Global Solution 2026.2 de Engenharia de Software, tema CitizenTech / Urban Risk Intelligence Platform. Região de referência: Mooca, São Paulo/SP.

**Todos os dados são fictícios.** Nenhum registro representa uma ocorrência real. O projeto não consulta sensores reais nem emite avisos oficiais.

**[Abrir o protótipo publicado](https://vitorpdb.github.io/GS-eng-software/)** · [Documentação em PDF](docs/radar-da-mooca-documentacao.pdf)

## Equipe

| Integrante | RM |
|---|---|
| Lucas Zolla Assis | 557952 |
| Lucas Baraldi Rodrigues | 555407 |
| Vitor Pantarotto de Brito | 554961 |

## Executar

Requer Node.js 22 ou superior. Não há dependências para instalar.

```sh
npm start
```

Abra <http://127.0.0.1:4173>. Mantenha o terminal aberto; `Ctrl+C` encerra o servidor. Não abra `index.html` diretamente com `file://`, porque o navegador restringe módulos JavaScript nesse modo.

Alternativa com Python instalado, executada na raiz do projeto:

```sh
python -m http.server 4173 --bind 127.0.0.1
```

## Testar

```sh
npm test
```

Em um executor que bloqueia a criação de processos de teste, com versão de Node que suporte a opção:

```sh
node --test --test-isolation=none tests/domain.test.js tests/presentation.test.js
```

Resultados e limites das verificações ficam em `docs/verificacao-qa.md`, quando disponível. Testes automatizados não comprovam disponibilidade ou escalabilidade de uma futura operação real.

## Percorrer a demonstração

1. Na visão geral, abra um alerta e consulte **Ver origem e confiança**.
2. Em **Registrar ocorrência**, crie um alagamento fictício, com impacto e urgência 3.
3. Abra **Acompanhar protocolo**. O relato nasce reportado e com confiança baixa.
4. No seletor do topo, mude para **Agente local** e acesse **Validação**; selecione o protocolo criado.
5. Preencha uma justificativa e inicie a validação. Use **Adicionar evidência simulada** para representar outras fontes.
6. Preencha a justificativa para confirmar e depois para emitir o alerta.
7. Confira a notificação e o vínculo com o evento.
8. Volte à validação para iniciar o monitoramento e encerrar o evento, sempre com justificativa. Inspecione o histórico completo.

O botão **Reiniciar demonstração** abre uma confirmação antes de restaurar os exemplos iniciais. Remove apenas a chave `radar-da-mooca:v1` deste navegador.

## Oito telas

| Tela | Rota |
|---|---|
| Visão geral | `#/painel` |
| Ocorrências e alertas | `#/alertas` |
| Detalhe | `#/detalhe/demo-alagamento` |
| Notificações | `#/notificacoes` |
| Registro comunitário | `#/registro` |
| Origem e confiança | `#/fontes/demo-alagamento` |
| Validação do agente | `#/validacao/demo-relato` |
| Histórico | `#/historico/demo-alagamento` |

A confirmação do envio é um estado da tela de registro; não foi contada como tela adicional.

## Arquitetura

```text
src/presentation/      HTML dinâmico, estilos, navegação e controlador
src/application/       Casos de uso com repositório e dados iniciais injetados
src/domain/            Risco, confiança, validação e transições
src/infrastructure/    Dados fictícios e persistência local com contingência
tests/                 Verificações das regras e casos de uso
docs/                  Especificação, UML, arquitetura, vídeo e checklist
scripts/               Servidor estático e geração de documentação
```

O domínio desconhece DOM e armazenamento. A aplicação usa contratos injetados; a composição dos adaptadores acontece na apresentação. A notificação é um efeito local do caso de uso de publicação. Camadas e injeção de dependências aplicam princípios de MVC e Clean/Hexagonal de forma proporcional ao protótipo, sem microsserviços.

## Regras reproduzíveis

- Gravidade: impacto + urgência, cada um de 1 a 3; soma 2 = baixa, 3/4 = moderada, 5/6 = alta.
- Confiança: +30 por existir fonte recente; +30 por pelo menos dois tipos recentes de fonte; +40 por validação de agente. Alta a partir de 80, média a partir de 50.
- Janela recente: de 0 a 30 minutos, inclusive; horários inválidos ou futuros não contam.
- Relógio fixo identificado na interface: **06/11/2026, 14h30 em São Paulo**.
- Emissão exige evento confirmado, fonte recente, confiança mínima 50 e gravidade moderada ou alta.
- Publicação gera uma única notificação interna por evento; não envia SMS, e-mail ou push.

Confiança é uma pontuação didática; não é uma probabilidade de acerto. A diversidade é medida por tipos de fonte, sem alegar independência estatística.

## Limites e privacidade

O estado pertence ao navegador e não é compartilhado entre computadores. Se o armazenamento falhar, a sessão continua em memória com aviso. A troca de perfil é demonstrativa: **não implementa autenticação nem autorização de produção**. Não informe dados pessoais nos textos livres. Não são solicitados nome, telefone, documento ou localização precisa do relator.

Disponibilidade e escalabilidade na especificação são metas de evolução; não foram comprovadas por este protótipo estático. As imagens do enunciado e os títulos das aulas orientaram o projeto; o conteúdo dos PDFs das aulas não foi fornecido.

## Publicar no GitHub Pages

No repositório, abra **Settings → Pages → Build and deployment → Deploy from a branch**. Selecione `main`, pasta `/(root)`, e salve. Aguarde o deploy e use o endereço confirmado pelo GitHub. Os caminhos relativos e as rotas por hash funcionam dentro de `/GS-eng-software/`.

O `.nojekyll` permite servir os arquivos estáticos diretamente. A publicação não exige banco, token ou variável secreta. Confira o protótipo e o vídeo em janela anônima antes de entregar. O vídeo e seu endereço ainda precisam ser produzidos pela equipe.

## Documentação

- `docs/especificacao.md`: problema, personas fictícias, 12 RF, 8 RNF, regras e rastreabilidade.
- `docs/diagramas/`: diagramas de sequência, estados e arquitetura, com fontes editáveis.
- `docs/radar-da-mooca-documentacao.pdf`: versão consolidada, quando gerada; a capa indica pendências de publicação e vídeo.
- `docs/roteiro-video.md`: demonstração com duração alvo abaixo de três minutos.
- `docs/checklist-entrega.md`: itens para a revisão e o envio final no Teams.

O trio deve revisar e compreender os artefatos elaborados com apoio de IA antes do envio.

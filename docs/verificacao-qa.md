# Registro de verificação

Versão local verificada em 06/11/2026. Este registro descreve o que foi executado; não representa certificação de acessibilidade, segurança ou operação real.

## Testes automatizados

Comando: `node --test --test-isolation=none tests/domain.test.js tests/presentation.test.js`

**Resultado: 15 testes, 15 aprovados, zero falhas**, após a correção da injeção de dependências e da ordenação. A opção sem isolamento foi usada porque este executor restringe a criação de subprocessos. O comando padrão `npm test` permanece disponível fora dessa restrição.

Cobertura: validação de formulário e inteiros; confiança por tipos de fonte; janela de atualidade e horários futuros; ciclo completo e notificação única; dados obsoletos; caminho de baixo risco e descarte; falhas de armazenamento e JSON corrompido; restauração e reinício restrito à chave própria; limite de eventos; ordenação; dependências entre camadas; notificações dos cenários iniciais; protocolo inexistente e recuperação; persistência vazia; aviso de armazenamento bloqueado; HTML hostil renderizado como texto.

Os quatro testes de apresentação importam o módulo real com um DOM mínimo. Complementam a verificação no navegador, sem substituí-la.

## Navegador

Verificação automatizada no Microsoft Edge em modo headless, usando servidor HTTP local. O fluxo executado foi:

1. Abrir painel e registrar um alagamento fictício de gravidade alta.
2. Receber protocolo e abrir o histórico.
3. Trocar para o perfil demonstrativo de agente e iniciar validação.
4. Acrescentar evidências fictícias, confirmar e emitir alerta.
5. Iniciar monitoramento e encerrar com justificativas.
6. Conferir o estado encerrado no histórico.
7. Abrir notificações, marcar uma como lida e confirmar a persistência após recarregar.
8. Visitar as oito telas em larguras de 360 e 1280 px e verificar a largura da página.
9. Restaurar o cenário inicial.

**Resultado:** fluxo concluído; zero erros JavaScript capturados; nenhuma rolagem horizontal da página nas combinações verificadas. A navegação móvel possui rolagem horizontal interna intencional.

Foram inspecionadas capturas da visão geral em 1440 px e 390 px, da origem/confiança e do histórico. A revisão visual independente aprovou a visão geral desktop/móvel e o código amostrado. Essa revisão não equivale a um teste de todas as tarefas com usuários reais.

## Conselho

Notas independentes para o pacote de escopo revisado: Arquiteto 5; QA 5 após correções; UX 5; Gerente Acadêmico 5; Inovação 5. Média aritmética **5,0**, superior ao corte de 4,5. As notas expressam pareceres de projeto; não preveem nota da instituição nem substituem as verificações acima.

## Publicação

Repositório publicado em https://github.com/VitorPDB/GS-eng-software. GitHub Pages confirmou estado `built`; a URL https://vitorpdb.github.io/GS-eng-software/ foi aberta em um navegador sem sessão autenticada do GitHub. A página exibiu painel, três notificações iniciais, fontes fictícias e links dos fluxos. Esse teste confirma acesso público ao protótipo, sem afirmar que um vídeo ainda não gravado foi verificado.

## Limites e pendências

- RNF01: a meta de atualização em até um segundo com cem registros e vinte medições ainda não tem relatório de desempenho específico.
- RNF02/RNF03: disponibilidade de produção e ingestão escalável são metas futuras, não medidas no protótipo.
- A inspeção visual e os estilos de foco não substituem uma auditoria completa de teclado, leitor de tela e contraste de todos os estados.
- Autenticação e autorização reais não fazem parte desta demonstração.
- O PDF foi renderizado e revisado visualmente; diagramas em SVG foram conferidos. As fontes PlantUML são editáveis e não foram compiladas por um runtime PlantUML nesta sessão.
- A gravação, publicação e verificação do vídeo ainda estão pendentes. Após inserir seu link na capa, revisar o PDF e o acesso final antes de enviar.

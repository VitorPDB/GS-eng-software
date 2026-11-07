export const DEMO_NOW = '2026-11-06T17:30:00.000Z';
const recent = '2026-11-06T17:20:00.000Z';
const source = (id, kind) => ({ id, name: `Fonte ${kind === 'sensor' ? 'sensorial' : kind === 'base_publica' ? 'pública' : 'comunitária'} fictícia — demonstração`, kind, observedAt: recent });

export function createSeed() {
  const definitions = [
    ['demo-alagamento', 'Alagamento simulado na Mooca', 'alagamento', 'Entorno da Rua da Mooca', 3, 3, 'alerta_emitido', true],
    ['demo-calor', 'Calor moderado simulado', 'calor', 'Entorno da Praça Visconde de Sousa Fontes', 2, 2, 'em_monitoramento', true],
    ['demo-servicos', 'Interrupção simulada de abastecimento', 'servicos', 'Entorno da Rua dos Trilhos', 2, 2, 'confirmado', true],
    ['demo-relato', 'Relato comunitário em análise', 'alagamento', 'Entorno da Rua Juventus', 2, 3, 'reportado', false],
    ['demo-encerrado', 'Ocorrência simulada encerrada', 'servicos', 'Entorno da Rua Itajaí', 1, 2, 'encerrado', true],
  ];
  const events = definitions.map(([id, title, category, location, impact, urgency, state, verified]) => ({
    id, title, category, location, impact, urgency, state, verified,
    description: 'Cenário fictício para demonstração acadêmica. Não representa uma ocorrência real.',
    sources: state === 'reportado' ? [source(`${id}-comunidade`, 'comunidade')] : [source(`${id}-sensor`, 'sensor'), source(`${id}-base`, 'base_publica')],
    history: [{ state: 'reportado', at: recent, note: 'Cenário fictício pré-carregado.' }, ...(state === 'reportado' ? [] : [{ state: 'em_validacao', at: recent, note: 'Verificação simulada das evidências.' }, { state: 'confirmado', at: recent, note: 'Confirmação simulada do agente.' }]), ...(state === 'alerta_emitido' || state === 'em_monitoramento' || state === 'encerrado' ? [{ state: 'alerta_emitido', at: recent, note: 'Publicação interna simulada.' }] : []), ...(state === 'em_monitoramento' || state === 'encerrado' ? [{ state: 'em_monitoramento', at: recent, note: 'Acompanhamento simulado.' }] : []), ...(state === 'encerrado' ? [{ state: 'encerrado', at: recent, note: 'Situação simulada normalizada.' }] : [])],
    createdAt: recent, updatedAt: recent,
  }));
  const notifications = events.filter(event => event.history.some(entry => entry.state === 'alerta_emitido')).map(event => ({
    id: `notification-${event.id}`, eventId: event.id, title: `Alerta simulado: ${event.title}`, message: 'Publicação interna fictícia. Consulte as evidências e o estado atual da ocorrência.', createdAt: event.history.find(entry => entry.state === 'alerta_emitido').at, read: false,
  }));
  return { events, notifications };
}

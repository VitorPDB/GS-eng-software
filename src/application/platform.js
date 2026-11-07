import { calculateEvent, validateReport, validateTransition } from '../domain/rules.js';
const clone = value => JSON.parse(JSON.stringify(value));
const LABELS = { alagamento: 'Alagamento', calor: 'Calor', servicos: 'Interrupção de serviços' };

export function createPlatform({ repository, clock, seedFactory } = {}) {
  if (!repository || typeof repository.load !== 'function' || typeof repository.save !== 'function' || typeof repository.reset !== 'function' || typeof clock !== 'function' || typeof seedFactory !== 'function') {
    throw new Error('Informe repositório, relógio e fábrica de dados da aplicação.');
  }
  let data = repository.load() || seedFactory();
  let counter = data.events.length;
  const now = () => {
    const result = clock();
    if (!Number.isFinite(Date.parse(result))) throw new Error('Relógio inválido.');
    return result;
  };
  const save = () => repository.save(data);
  const find = id => {
    const event = data.events.find(item => item.id === id);
    if (!event) throw new Error('Ocorrência não encontrada.');
    return event;
  };
  const calculated = event => clone(calculateEvent(event, now()));
  save();
  return {
    listEvents() {
      const rank = { alto: 0, moderado: 1, baixo: 2 };
      return data.events.map(calculated).sort((a, b) => rank[a.severity] - rank[b.severity] || Date.parse(b.createdAt) - Date.parse(a.createdAt) || (a.id < b.id ? -1 : a.id > b.id ? 1 : 0));
    },
    getEvent(id) { return calculated(find(id)); },
    getNotifications() { return clone(data.notifications); },
    markRead(id) {
      const item = data.notifications.find(notification => notification.id === id);
      if (!item) throw new Error('Notificação não encontrada.');
      item.read = true; save(); return clone(item);
    },
    createReport(input) {
      const report = validateReport(input);
      if (data.events.length >= 100) throw new Error('Limite de 100 ocorrências da demonstração atingido. Reinicie os dados para continuar.');
      const at = now();
      let id;
      do { id = `relato-${Date.parse(at)}-${++counter}`; } while (data.events.some(event => event.id === id));
      const event = { ...report, id, title: `${LABELS[report.category]} — ${report.location}`, state: 'reportado', verified: false, sources: [{ id: `${id}-comunidade`, name: 'Registro comunitário fictício — demonstração', kind: 'comunidade', observedAt: at }], history: [{ state: 'reportado', at, note: 'Relato registrado na demonstração.' }], createdAt: at, updatedAt: at };
      data.events.unshift(event); save(); return calculated(event);
    },
    transition(id, target, note) {
      const event = find(id);
      const at = now();
      validateTransition(event, target, note, at);
      const trimmedNote = note.trim().slice(0, 400);
      event.state = target; event.updatedAt = at;
      if (target === 'confirmado') event.verified = true;
      event.history.push({ state: target, at, note: trimmedNote });
      if (target === 'alerta_emitido' && !data.notifications.some(item => item.eventId === id)) {
        data.notifications.unshift({ id: `notification-${id}`, eventId: id, title: `Alerta simulado: ${event.title}`, message: `Risco ${calculateEvent(event, at).severity}. Consulte a origem e a confiança dos dados.`, createdAt: at, read: false });
      }
      save(); return calculated(event);
    },
    addDemoEvidence(id) {
      const event = find(id);
      if (['encerrado', 'descartado'].includes(event.state)) throw new Error('Ocorrência finalizada não recebe novas evidências.');
      const at = now();
      for (const kind of ['sensor', 'base_publica']) {
        const source = { id: `${id}-demo-${kind}`, name: `${kind === 'sensor' ? 'Sensor' : 'Base pública'} fictício(a) — evidência simulada`, kind, observedAt: at };
        const existing = event.sources.findIndex(item => item.id === source.id);
        if (existing >= 0) event.sources[existing] = source; else event.sources.push(source);
      }
      event.updatedAt = at;
      event.history.push({ state: event.state, at, note: 'Adicionadas evidências explicitamente simuladas; confirmação continua dependendo do agente.' });
      save(); return calculated(event);
    },
    reset() { repository.reset(); data = seedFactory(); counter = data.events.length; save(); return this.listEvents(); },
    getStorageWarning() { return repository.getWarning?.() || null; },
  };
}

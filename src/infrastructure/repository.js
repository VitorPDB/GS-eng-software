import { CATEGORIES, STATES, SOURCE_KINDS } from '../domain/rules.js';
export const STORAGE_KEY = 'radar-da-mooca:v1';
const clone = value => JSON.parse(JSON.stringify(value));
const validDate = value => typeof value === 'string' && Number.isFinite(Date.parse(value));
function sanitize(snapshot) {
  if (!snapshot || !Array.isArray(snapshot.events) || !Array.isArray(snapshot.notifications)) throw new Error('Formato inválido.');
  const ids = new Set();
  const events = snapshot.events.slice(0, 100).filter(event => {
    if (!event || typeof event.id !== 'string' || !event.id || ids.has(event.id) || !CATEGORIES.includes(event.category) || !STATES.includes(event.state)) return false;
    if (!['title', 'location', 'description'].every(key => typeof event[key] === 'string') || !['impact', 'urgency'].every(key => Number.isInteger(event[key]) && event[key] >= 1 && event[key] <= 3)) return false;
    if (!validDate(event.createdAt) || !validDate(event.updatedAt) || !Array.isArray(event.sources) || !Array.isArray(event.history)) return false;
    ids.add(event.id); return true;
  }).map(event => ({
    id: event.id, title: event.title.slice(0, 160), category: event.category, location: event.location.slice(0, 80), description: event.description.slice(0, 400), impact: event.impact, urgency: event.urgency, state: event.state, verified: event.verified === true, createdAt: event.createdAt, updatedAt: event.updatedAt,
    sources: event.sources.filter(source => source && typeof source.id === 'string' && typeof source.name === 'string' && SOURCE_KINDS.includes(source.kind) && validDate(source.observedAt)).slice(0, 30).map(source => ({ id: source.id, name: source.name.slice(0, 160), kind: source.kind, observedAt: source.observedAt })),
    history: event.history.filter(entry => entry && STATES.includes(entry.state) && validDate(entry.at) && typeof entry.note === 'string').slice(-100).map(entry => ({ state: entry.state, at: entry.at, note: entry.note.slice(0, 400) })),
  }));
  const notificationIds = new Set();
  const notifications = snapshot.notifications.filter(item => {
    if (!item || typeof item.id !== 'string' || notificationIds.has(item.id) || !ids.has(item.eventId) || typeof item.title !== 'string' || !validDate(item.createdAt)) return false;
    notificationIds.add(item.id); return true;
  }).slice(0, 100).map(item => {
    return { id: item.id, eventId: item.eventId, title: item.title.slice(0, 160), message: typeof item.message === 'string' ? item.message.slice(0, 400) : '', createdAt: item.createdAt, read: item.read === true };
  });
  if (snapshot.events.length && !events.length) throw new Error('Eventos salvos inválidos.');
  return { events, notifications };
}

export function createRepository(storage = null) {
  let memory = null;
  let warning = null;
  let persistent = storage;
  return {
    load() {
      if (persistent) {
        try {
          const raw = persistent.getItem(STORAGE_KEY);
          if (raw !== null) memory = sanitize(JSON.parse(raw));
        } catch {
          warning = 'O armazenamento local está indisponível ou corrompido. A demonstração continuará em memória.';
          persistent = null;
        }
      }
      return memory === null ? null : clone(memory);
    },
    save(snapshot) {
      memory = sanitize(snapshot);
      if (persistent) {
        try { persistent.setItem(STORAGE_KEY, JSON.stringify(memory)); }
        catch { warning = 'Não foi possível salvar neste navegador. Os dados desta sessão continuam em memória.'; persistent = null; }
      }
    },
    reset() {
      memory = null;
      if (persistent) {
        try { persistent.removeItem(STORAGE_KEY); }
        catch { warning = 'Não foi possível limpar o armazenamento; a demonstração foi reiniciada em memória.'; persistent = null; }
      }
    },
    getWarning() { return warning; },
  };
}

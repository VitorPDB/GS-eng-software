import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { calculateEvent, FRESH_WINDOW_MS } from '../src/domain/rules.js';
import { createPlatform } from '../src/application/platform.js';
import { createRepository, STORAGE_KEY } from '../src/infrastructure/repository.js';
import { DEMO_NOW, createSeed } from '../src/infrastructure/seed.js';

const input = { category: 'alagamento', location: 'Rua da Mooca', description: 'Água acumulada perto da esquina.', impact: 3, urgency: 2 };
const platform = () => createPlatform({ repository: createRepository(), clock: () => DEMO_NOW, seedFactory: createSeed });

test('valida campos, enums e inteiros sem criar ocorrência inválida', () => {
  const app = platform(); const initial = app.listEvents().length;
  for (const invalid of [{ category: 'outro' }, { location: 'a' }, { description: 'curta' }, { impact: 1.5 }, { urgency: '3' }]) assert.throws(() => app.createReport({ ...input, ...invalid }));
  assert.equal(app.listEvents().length, initial);
  const event = app.createReport(input);
  assert.equal(event.state, 'reportado'); assert.equal(event.confidence.score, 30); assert.equal(event.severity, 'alto');
});

test('confiança usa tipos distintos e fontes recentes; janela inclui limite e exclui futuro', () => {
  const app = platform(); const event = app.getEvent('demo-alagamento');
  assert.equal(event.confidence.score, 100);
  const old = new Date(Date.parse(DEMO_NOW) + FRESH_WINDOW_MS + 1).toISOString();
  assert.equal(calculateEvent(event, old).confidence.score, 40);
  assert.equal(calculateEvent(event, old).stale, true);
  const source = { id: 's', kind: 'sensor', observedAt: DEMO_NOW };
  const base = { ...event, verified: false, sources: [source, { ...source, id: 's2' }] };
  assert.equal(calculateEvent(base, DEMO_NOW).confidence.score, 30);
  assert.equal(calculateEvent(base, new Date(Date.parse(DEMO_NOW) + FRESH_WINDOW_MS).toISOString()).stale, false);
  assert.equal(calculateEvent(base, new Date(Date.parse(DEMO_NOW) - 1).toISOString()).confidence.score, 0);
});

test('fluxo completo publica exatamente uma notificação e encerramento não publica', () => {
  const app = platform(); const event = app.createReport(input); const count = app.getNotifications().length;
  assert.throws(() => app.transition(event.id, 'confirmado', 'verificado'));
  app.transition(event.id, 'em_validacao', 'Análise iniciada.');
  assert.throws(() => app.transition(event.id, 'confirmado', ' '));
  app.transition(event.id, 'confirmado', 'Relato verificado pelo agente.');
  assert.equal(app.getEvent(event.id).confidence.score, 70);
  app.transition(event.id, 'alerta_emitido', 'Risco confirmado e recente.');
  assert.equal(app.getNotifications().length, count + 1);
  assert.throws(() => app.transition(event.id, 'alerta_emitido', 'Repetir.'));
  app.transition(event.id, 'em_monitoramento', 'Acompanhando.');
  app.transition(event.id, 'encerrado', 'Situação normalizada.');
  assert.equal(app.getNotifications().length, count + 1);
  app.markRead(`notification-${event.id}`);
  assert.equal(app.getNotifications().find(item => item.eventId === event.id).read, true);
});

test('fonte obsoleta bloqueia confirmação e publicação; evidência simulada não confirma sozinha', () => {
  let at = DEMO_NOW;
  const app = createPlatform({ repository: createRepository(), clock: () => at, seedFactory: createSeed });
  const event = app.createReport(input);
  app.transition(event.id, 'em_validacao', 'Análise.');
  at = '2026-11-06T18:10:00.000Z';
  assert.throws(() => app.transition(event.id, 'confirmado', 'Tentativa sem fonte atual.'));
  const enriched = app.addDemoEvidence(event.id);
  assert.equal(enriched.state, 'em_validacao'); assert.equal(enriched.verified, false); assert.equal(enriched.confidence.score, 60);
  app.transition(event.id, 'confirmado', 'Evidências atuais conferidas.');
  at = '2026-11-06T19:00:00.000Z';
  assert.throws(() => app.transition(event.id, 'alerta_emitido', 'Tentativa obsoleta.'));
});

test('baixo risco segue monitoramento sem publicar e descarte exige motivo', () => {
  const app = platform(); const event = app.createReport({ ...input, impact: 1, urgency: 1 });
  app.transition(event.id, 'em_validacao', 'Análise.'); app.transition(event.id, 'confirmado', 'Verificado.');
  assert.throws(() => app.transition(event.id, 'alerta_emitido', 'Baixo risco.'));
  app.transition(event.id, 'em_monitoramento', 'Acompanhar baixo risco.');
  const other = app.createReport(input);
  assert.throws(() => app.transition(other.id, 'descartado', ''));
  app.transition(other.id, 'descartado', 'Duplicidade verificada.');
  assert.throws(() => app.transition(other.id, 'em_validacao', 'Reabrir.'));
});

test('repositório tolera storage bloqueado, escrita sem espaço e JSON corrompido', () => {
  for (const storage of [
    { getItem() { throw new Error('blocked'); } },
    { getItem() { return '{'; } },
    { getItem() { return null; }, setItem() { throw new Error('quota'); } },
  ]) {
    const app = createPlatform({ repository: createRepository(storage), clock: () => DEMO_NOW, seedFactory: createSeed });
    assert.equal(app.listEvents().length, 5); assert.ok(app.getStorageWarning());
    const event = app.createReport(input); assert.equal(app.getEvent(event.id).state, 'reportado');
  }
});

test('persistência restaura dados e reset remove apenas a chave própria', () => {
  const entries = new Map([['outra-chave', 'preservar']]);
  const storage = { getItem: key => entries.get(key) ?? null, setItem: (key, value) => entries.set(key, value), removeItem: key => entries.delete(key) };
  const first = createPlatform({ repository: createRepository(storage), clock: () => DEMO_NOW, seedFactory: createSeed });
  const event = first.createReport(input);
  const second = createPlatform({ repository: createRepository(storage), clock: () => DEMO_NOW, seedFactory: createSeed });
  assert.equal(second.getEvent(event.id).state, 'reportado');
  second.reset();
  assert.equal(second.listEvents().length, 5); assert.equal(entries.get('outra-chave'), 'preservar'); assert.ok(entries.has(STORAGE_KEY));
});

test('limite de eventos impede crescimento ilimitado', () => {
  const app = platform();
  for (let i = 5; i < 100; i++) app.createReport(input);
  assert.throws(() => app.createReport(input), /Limite/);
});

test('priorização ordena risco, data decrescente e identificador estável', () => {
  const base = createSeed().events[0];
  const definitions = [
    ['moderado', 2, 2, DEMO_NOW], ['baixo', 1, 1, DEMO_NOW],
    ['alto-antigo', 3, 3, '2026-11-06T17:00:00.000Z'],
    ['alto-b', 3, 3, DEMO_NOW], ['alto-a', 3, 3, DEMO_NOW],
  ];
  const seedFactory = () => ({ events: definitions.map(([id, impact, urgency, createdAt]) => ({ ...base, id, impact, urgency, createdAt })), notifications: [] });
  const app = createPlatform({ repository: createRepository(), clock: () => DEMO_NOW, seedFactory });
  assert.deepEqual(app.listEvents().map(event => event.id), ['alto-a', 'alto-b', 'alto-antigo', 'moderado', 'baixo']);
});

test('aplicação exige dependências injetadas e não importa infraestrutura ou apresentação', () => {
  assert.throws(() => createPlatform(), /repositório/);
  const source = readFileSync(new URL('../src/application/platform.js', import.meta.url), 'utf8');
  assert.doesNotMatch(source, /(?:from\s*|import\s*)['"][^'"]*(?:infrastructure|presentation)/);
});

test('cada publicação histórica do seed tem exatamente uma notificação', () => {
  const { events, notifications } = createSeed();
  for (const event of events) {
    const published = event.history.some(entry => entry.state === 'alerta_emitido');
    assert.equal(notifications.filter(item => item.eventId === event.id).length, published ? 1 : 0);
  }
});

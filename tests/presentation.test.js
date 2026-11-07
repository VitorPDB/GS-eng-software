import test from 'node:test';
import assert from 'node:assert/strict';
import { createSeed } from '../src/infrastructure/seed.js';

let importNumber = 0;

// DOM mínimo: executa o módulo real, observa seu HTML e dispara hashchange.
// Não substitui os testes de navegação e layout em navegador.
async function withPresentation({ hash, snapshot = null, blockedStorage = false }, verify) {
  const original = Object.fromEntries(['window', 'document', 'location'].map(key => [key, Object.getOwnPropertyDescriptor(globalThis, key)]));
  const listeners = new Map();
  const element = () => ({ innerHTML: '', addEventListener() {}, focus() {} });
  const root = element();
  const nodes = new Map([['#app', root], ['#profile', element()], ['#main', element()]]);
  const entries = new Map(snapshot === null ? [] : [['radar-da-mooca:v1', JSON.stringify(snapshot)]]);
  const windowMock = { addEventListener: (name, handler) => listeners.set(name, handler), scrollTo() {} };
  if (blockedStorage) Object.defineProperty(windowMock, 'localStorage', { get() { throw new Error('Storage denied'); } });
  else windowMock.localStorage = { getItem: key => entries.get(key) ?? null, setItem: (key, value) => entries.set(key, value), removeItem: key => entries.delete(key) };
  globalThis.window = windowMock;
  globalThis.document = { querySelector: selector => nodes.get(selector) ?? null, title: '' };
  globalThis.location = { hash };
  try {
    await import(`../src/presentation/app.js?qa=${++importNumber}`);
    await verify({ html: () => root.innerHTML, navigate(nextHash) { globalThis.location.hash = nextHash; listeners.get('hashchange')(); } });
  } finally {
    for (const [key, descriptor] of Object.entries(original)) {
      if (descriptor) Object.defineProperty(globalThis, key, descriptor);
      else delete globalThis[key];
    }
  }
}

test('link com protocolo inexistente mostra recuperação e permite continuar navegando', async () => {
  await withPresentation({ hash: '#/detalhe/inexistente' }, ({ html, navigate }) => {
    assert.match(html(), /Ocorrência não encontrada/);
    assert.match(html(), /Voltar à lista/);
    navigate('#/painel');
    assert.match(html(), /O que acontece na Mooca/);
  });
});

test('persistência vazia oferece recuperação em todas as telas dependentes de ocorrência', async () => {
  await withPresentation({ hash: '#/painel', snapshot: { events: [], notifications: [] } }, ({ html, navigate }) => {
    for (const page of ['detalhe', 'fontes', 'validacao', 'historico']) {
      navigate(`#/${page}`);
      assert.match(html(), /Nenhuma ocorrência disponível/);
      assert.match(html(), /Registrar ocorrência/);
    }
    navigate('#/registro');
    assert.match(html(), /id="report-form"/);
  });
});

test('getter de armazenamento bloqueado mantém painel e avisa sobre memória', async () => {
  await withPresentation({ hash: '#/painel', blockedStorage: true }, ({ html }) => {
    assert.match(html(), /O que acontece na Mooca/);
    assert.match(html(), /armazenamento local foi bloqueado/);
    assert.match(html(), /role="status"/);
    assert.match(html(), /podem se perder ao recarregar/);
  });
});

test('conteúdo salvo contendo marcação aparece escapado no detalhe e histórico', async () => {
  const snapshot = createSeed();
  const payload = '<img src=x onerror="alert(1)">';
  snapshot.events[0].description = payload;
  snapshot.events[0].history[0].note = payload;
  await withPresentation({ hash: '#/detalhe/demo-alagamento', snapshot }, ({ html, navigate }) => {
    assert.ok(!html().includes(payload));
    assert.match(html(), /&lt;img src=x onerror=&quot;alert\(1\)&quot;&gt;/);
    navigate('#/historico/demo-alagamento');
    assert.ok(!html().includes(payload));
    assert.match(html(), /&lt;img src=x onerror=&quot;alert\(1\)&quot;&gt;/);
  });
});

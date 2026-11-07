export const CATEGORIES = ['alagamento', 'calor', 'servicos'];
export const STATES = ['reportado', 'em_validacao', 'confirmado', 'alerta_emitido', 'em_monitoramento', 'encerrado', 'descartado'];
export const SOURCE_KINDS = ['comunidade', 'sensor', 'base_publica'];
export const FRESH_WINDOW_MS = 30 * 60 * 1000;

export function isFresh(source, now) {
  const age = Date.parse(now) - Date.parse(source.observedAt);
  return Number.isFinite(age) && age >= 0 && age <= FRESH_WINDOW_MS;
}

export function calculateEvent(event, now) {
  const fresh = event.sources.filter(source => isFresh(source, now));
  const independentCount = new Set(fresh.map(source => source.kind)).size;
  const score = (fresh.length ? 30 : 0) + (independentCount >= 2 ? 30 : 0) + (event.verified ? 40 : 0);
  const sum = event.impact + event.urgency;
  return {
    ...event,
    severity: sum >= 5 ? 'alto' : sum >= 3 ? 'moderado' : 'baixo',
    confidence: { score, level: score >= 80 ? 'alta' : score >= 50 ? 'media' : 'baixa', freshCount: fresh.length, independentCount },
    stale: fresh.length === 0,
  };
}

export function validateReport(input) {
  if (!input || !CATEGORIES.includes(input.category)) throw new Error('Selecione uma categoria válida.');
  const location = typeof input.location === 'string' ? input.location.trim() : '';
  const description = typeof input.description === 'string' ? input.description.trim() : '';
  if (location.length < 3 || location.length > 80) throw new Error('Informe uma localização aproximada entre 3 e 80 caracteres.');
  if (description.length < 10 || description.length > 400) throw new Error('Descreva a ocorrência usando entre 10 e 400 caracteres.');
  for (const key of ['impact', 'urgency']) {
    if (!Number.isInteger(input[key]) || input[key] < 1 || input[key] > 3) throw new Error('Impacto e urgência devem ser números inteiros de 1 a 3.');
  }
  return { category: input.category, location, description, impact: input.impact, urgency: input.urgency };
}

export function validateTransition(event, target, note, now) {
  if (typeof note !== 'string' || !note.trim()) throw new Error('Informe o motivo da mudança de estado.');
  const paths = {
    reportado: ['em_validacao', 'descartado'],
    em_validacao: ['confirmado', 'descartado'],
    confirmado: ['alerta_emitido', 'em_monitoramento'],
    alerta_emitido: ['em_monitoramento'],
    em_monitoramento: ['encerrado'],
    encerrado: [], descartado: [],
  };
  if (!paths[event.state]?.includes(target)) throw new Error('Transição não permitida para o estado atual.');
  const calculated = calculateEvent(event, now);
  if (target === 'confirmado' && calculated.stale) throw new Error('Confirmação exige ao menos uma fonte recente.');
  if (target === 'alerta_emitido' && (calculated.stale || calculated.confidence.score < 50 || calculated.severity === 'baixo')) {
    throw new Error('Publicação exige fonte recente, confiança mínima de 50 e risco moderado ou alto.');
  }
  if (event.state === 'confirmado' && target === 'em_monitoramento' && calculated.severity !== 'baixo') {
    throw new Error('Risco moderado ou alto confirmado deve passar pela emissão do alerta.');
  }
}

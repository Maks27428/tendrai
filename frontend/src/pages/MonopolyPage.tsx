import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getTenders, checkMonopoly } from '../api/client';
import type { TenderListItem, MonopolyResult } from '../api/client';
import { Shield, ShieldAlert, ShieldCheck, AlertTriangle, CheckCircle, Info, ArrowLeft, Search } from 'lucide-react';

const FLAG_LABELS: Record<string, string> = {
  same_phone: 'Совпадение телефонов',
  same_email: 'Совпадение email',
  same_iin: 'Совпадение ИИН/БИН',
  same_address: 'Совпадение адресов',
  same_specs: 'Идентичные ТЗ',
  brand_lock: 'Привязка к бренду',
  tight_deadline: 'Сжатые сроки',
  split_purchase: 'Дробление закупок',
  same_bank: 'Совпадение банковских реквизитов',
  other: 'Другое',
};

function ScoreGauge({ score, verdict }: { score: number; verdict: string }) {
  const color = verdict === 'critical' ? 'text-danger' : verdict === 'suspicious' ? 'text-warning' : 'text-success';
  const bg = verdict === 'critical' ? 'bg-danger/20' : verdict === 'suspicious' ? 'bg-warning/20' : 'bg-success/20';
  const label = verdict === 'critical' ? 'Критично' : verdict === 'suspicious' ? 'Подозрительно' : 'Чисто';

  return (
    <div className={`flex flex-col items-center gap-3 p-8 rounded-2xl ${bg}`}>
      <Shield className={`w-12 h-12 ${color}`} />
      <div className={`text-5xl font-bold ${color}`}>{score}</div>
      <div className="text-sm text-text-muted">из 100</div>
      <div className={`text-lg font-semibold ${color}`}>{label}</div>
    </div>
  );
}

export default function MonopolyPage() {
  const [tenders, setTenders] = useState<TenderListItem[]>([]);
  const [selected, setSelected] = useState<Set<number>>(new Set());
  const [loading, setLoading] = useState(true);
  const [checking, setChecking] = useState(false);
  const [result, setResult] = useState<MonopolyResult | null>(null);
  const [error, setError] = useState('');

  useEffect(() => {
    getTenders()
      .then((data) => setTenders(data.filter((t) => t.status === 'completed')))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const toggle = (id: number) => {
    setSelected((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
    setResult(null);
  };

  const handleCheck = async () => {
    setChecking(true);
    setError('');
    setResult(null);
    try {
      const res = await checkMonopoly([...selected]);
      setResult(res);
    } catch {
      setError('Ошибка проверки. Убедитесь, что LLM_API_KEY настроен.');
    } finally {
      setChecking(false);
    }
  };

  const severityIcon = (s: string) => {
    if (s === 'critical') return <ShieldAlert className="w-5 h-5 text-danger shrink-0" />;
    if (s === 'warning') return <AlertTriangle className="w-5 h-5 text-warning shrink-0" />;
    return <Info className="w-5 h-5 text-primary shrink-0" />;
  };

  return (
    <div className="max-w-5xl mx-auto">
      <Link to="/" className="inline-flex items-center gap-2 text-sm text-text-muted hover:text-text mb-6">
        <ArrowLeft className="w-4 h-4" /> Назад
      </Link>

      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-text mb-2">Проверка на монополию</h1>
        <p className="text-text-muted">
          Выберите 2+ тендера — AI проверит на признаки сговора, монополии и коррупции
        </p>
      </div>

      {/* Tender selection */}
      <div className="mb-6">
        <h2 className="text-sm font-semibold text-text-muted mb-3">
          Выберите тендеры для проверки ({selected.size} выбрано)
        </h2>
        {loading ? (
          <div className="text-center py-8 text-text-muted">Загрузка...</div>
        ) : tenders.length === 0 ? (
          <div className="text-center py-8 border border-dashed border-border rounded-xl">
            <p className="text-text-muted">Нет проанализированных тендеров. <Link to="/" className="text-primary">Загрузите PDF</Link></p>
          </div>
        ) : (
          <div className="space-y-2">
            {tenders.map((t) => (
              <button
                key={t.id}
                onClick={() => toggle(t.id)}
                className={`w-full flex items-center gap-4 p-4 rounded-xl border transition-all text-left ${
                  selected.has(t.id)
                    ? 'border-primary bg-primary/10'
                    : 'border-border bg-surface-2 hover:border-primary/50'
                }`}
              >
                <div className={`w-5 h-5 rounded border-2 flex items-center justify-center shrink-0 ${
                  selected.has(t.id) ? 'border-primary bg-primary' : 'border-text-muted'
                }`}>
                  {selected.has(t.id) && <CheckCircle className="w-4 h-4 text-white" />}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-text truncate">{t.title}</p>
                  <p className="text-xs text-text-muted">
                    {t.summary?.customer} · {t.summary?.amount}
                  </p>
                </div>
                {t.risk_score !== null && (
                  <span className={`text-xs px-2 py-1 rounded-md ${
                    t.risk_score > 60 ? 'bg-danger/10 text-danger' :
                    t.risk_score > 30 ? 'bg-warning/10 text-warning' :
                    'bg-success/10 text-success'
                  }`}>
                    Риск {t.risk_score}
                  </span>
                )}
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Check button */}
      <button
        onClick={handleCheck}
        disabled={selected.size < 2 || checking}
        className="w-full py-4 bg-primary hover:bg-primary/90 text-white font-semibold rounded-xl transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-3"
      >
        {checking ? (
          <>
            <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
            AI анализирует...
          </>
        ) : (
          <>
            <Search className="w-5 h-5" />
            Проверить на монополию ({selected.size} тендеров)
          </>
        )}
      </button>

      {error && (
        <div className="mt-4 p-4 bg-danger/10 border border-danger/30 rounded-xl flex items-center gap-3">
          <AlertTriangle className="w-5 h-5 text-danger shrink-0" />
          <p className="text-sm text-danger">{error}</p>
        </div>
      )}

      {/* Results */}
      {result && (
        <div className="mt-8 space-y-6 animate-in fade-in duration-500">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Score */}
            <ScoreGauge score={result.monopoly_score} verdict={result.verdict} />

            {/* Summary + Recommendations */}
            <div className="md:col-span-2 space-y-4">
              <div className="p-5 bg-surface-2 border border-border rounded-xl">
                <h3 className="text-sm font-semibold text-text mb-2">Заключение</h3>
                <p className="text-sm text-text-muted">{result.summary}</p>
              </div>
              {result.recommendations.length > 0 && (
                <div className="p-5 bg-surface-2 border border-border rounded-xl">
                  <h3 className="text-sm font-semibold text-text mb-2">Рекомендации</h3>
                  <ul className="space-y-1">
                    {result.recommendations.map((r, i) => (
                      <li key={i} className="flex gap-2 text-sm text-text-muted">
                        <ShieldCheck className="w-4 h-4 text-primary shrink-0 mt-0.5" />
                        {r}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>

          {/* Flags */}
          {result.flags.length > 0 && (
            <div>
              <h3 className="text-base font-semibold text-text mb-4">
                Обнаруженные признаки ({result.flags.length})
              </h3>
              <div className="space-y-3">
                {result.flags.map((flag, i) => (
                  <div
                    key={i}
                    className={`p-4 rounded-xl border ${
                      flag.severity === 'critical' ? 'border-danger/30 bg-danger/5' :
                      flag.severity === 'warning' ? 'border-warning/30 bg-warning/5' :
                      'border-border bg-surface-2'
                    }`}
                  >
                    <div className="flex items-start gap-3">
                      {severityIcon(flag.severity)}
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1">
                          <span className="text-sm font-semibold text-text">
                            {FLAG_LABELS[flag.type] || flag.type}
                          </span>
                          <span className={`text-xs px-2 py-0.5 rounded ${
                            flag.severity === 'critical' ? 'bg-danger/20 text-danger' :
                            flag.severity === 'warning' ? 'bg-warning/20 text-warning' :
                            'bg-primary/20 text-primary'
                          }`}>
                            {flag.severity === 'critical' ? 'Критично' : flag.severity === 'warning' ? 'Внимание' : 'Инфо'}
                          </span>
                        </div>
                        <p className="text-sm text-text-muted mb-2">{flag.description}</p>
                        {flag.evidence && (
                          <div className="text-xs font-mono bg-surface-1 p-2 rounded border border-border text-text-muted">
                            {flag.evidence}
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

import { useState, useCallback } from 'react';
import { Search, ExternalLink, Banknote, Building2, Tag, Loader2, SearchX, Sparkles } from 'lucide-react';
import { searchGoszakup } from '../api/client';
import type { GoszakupTender } from '../api/client';

const QUICK_FILTERS = [
  'IT оборудование',
  'Мебель',
  'Строительство',
  'Медицина',
  'Транспорт',
  'Продукты питания',
  'Канцтовары',
  'Охрана',
];

function formatAmount(amount: number): string {
  if (!amount) return '—';
  if (amount >= 1_000_000) {
    return `${(amount / 1_000_000).toFixed(1)} млн ₸`;
  }
  if (amount >= 1_000) {
    return `${(amount / 1_000).toFixed(0)} тыс ₸`;
  }
  return `${amount.toFixed(0)} ₸`;
}

function statusColor(status: string): string {
  const s = status.toLowerCase();
  if (s.includes('прием заявок') || s.includes('опубликован')) return 'bg-emerald-500/15 text-emerald-400 border-emerald-500/30';
  if (s.includes('завершен') || s.includes('итоги')) return 'bg-sky-500/15 text-sky-400 border-sky-500/30';
  if (s.includes('отмен')) return 'bg-red-500/15 text-red-400 border-red-500/30';
  return 'bg-zinc-500/15 text-zinc-400 border-zinc-500/30';
}

export default function SearchPage() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<GoszakupTender[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);
  const [error, setError] = useState('');
  const [page, setPage] = useState(1);

  const doSearch = useCallback(async (q: string, p: number = 1) => {
    if (!q.trim()) return;
    setLoading(true);
    setError('');
    setSearched(true);
    setQuery(q);
    setPage(p);
    try {
      const data = await searchGoszakup(q.trim(), p);
      setResults(data.results);
      setTotal(data.total);
      if (data.error) setError(data.error);
    } catch {
      setError('Не удалось выполнить поиск. Попробуйте позже.');
      setResults([]);
    } finally {
      setLoading(false);
    }
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    doSearch(query, 1);
  };

  return (
    <div className="max-w-5xl mx-auto">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-text mb-2">
          Поиск тендеров
        </h1>
        <p className="text-text-muted">
          Найдите актуальные тендеры на goszakup.gov.kz прямо здесь
        </p>
      </div>

      {/* Search bar */}
      <form onSubmit={handleSubmit} className="relative mb-5">
        <div className="relative">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-text-muted pointer-events-none" />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Введите название тендера, товара или услуги..."
            className="w-full pl-12 pr-32 py-4 bg-surface-2 border border-border rounded-2xl text-text placeholder:text-text-muted/50 focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary/30 text-base transition-all"
          />
          <button
            type="submit"
            disabled={loading || !query.trim()}
            className="absolute right-2 top-1/2 -translate-y-1/2 px-6 py-2.5 bg-primary hover:bg-primary/90 disabled:opacity-40 disabled:cursor-not-allowed text-white font-medium rounded-xl transition-all text-sm"
          >
            {loading ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              'Найти'
            )}
          </button>
        </div>
      </form>

      {/* Quick filters */}
      <div className="flex flex-wrap gap-2 mb-8">
        {QUICK_FILTERS.map((filter) => (
          <button
            key={filter}
            onClick={() => {
              setQuery(filter);
              doSearch(filter, 1);
            }}
            disabled={loading}
            className="px-3.5 py-1.5 text-xs font-medium bg-surface-2 hover:bg-primary/15 hover:text-primary border border-border hover:border-primary/30 rounded-full transition-all disabled:opacity-50"
          >
            {filter}
          </button>
        ))}
      </div>

      {/* Error */}
      {error && (
        <div className="mb-6 p-4 bg-danger/10 border border-danger/30 rounded-xl text-sm text-danger">
          {error}
        </div>
      )}

      {/* Results */}
      {loading ? (
        <div className="space-y-4">
          {[1, 2, 3, 4, 5].map((i) => (
            <div key={i} className="p-5 bg-surface-2 border border-border rounded-2xl animate-pulse">
              <div className="h-5 bg-border rounded w-3/4 mb-3" />
              <div className="h-4 bg-border rounded w-1/2 mb-4" />
              <div className="flex gap-3">
                <div className="h-7 bg-border rounded-lg w-24" />
                <div className="h-7 bg-border rounded-lg w-32" />
                <div className="h-7 bg-border rounded-lg w-28" />
              </div>
            </div>
          ))}
        </div>
      ) : results.length > 0 ? (
        <>
          <div className="flex items-center justify-between mb-4">
            <p className="text-sm text-text-muted">
              Найдено: <span className="text-text font-medium">{total > 0 ? total.toLocaleString('ru-RU') : results.length}</span> тендеров
            </p>
            {page > 1 && (
              <span className="text-xs text-text-muted">Страница {page}</span>
            )}
          </div>

          <div className="space-y-3">
            {results.map((tender, idx) => (
              <div
                key={`${tender.announce_id}-${idx}`}
                className="group p-5 bg-surface-2 border border-border rounded-2xl hover:border-primary/40 transition-all"
              >
                {/* Title + Status */}
                <div className="flex items-start justify-between gap-4 mb-3">
                  <div className="flex-1 min-w-0">
                    <h3 className="text-sm font-semibold text-text leading-snug line-clamp-2">
                      {tender.title || tender.description || 'Без названия'}
                    </h3>
                    {tender.description && tender.description !== tender.title && (
                      <p className="text-xs text-text-muted mt-1 line-clamp-1">{tender.description}</p>
                    )}
                  </div>
                  {tender.status && (
                    <span className={`shrink-0 text-xs px-2.5 py-1 rounded-lg border font-medium ${statusColor(tender.status)}`}>
                      {tender.status}
                    </span>
                  )}
                </div>

                {/* Customer */}
                {tender.customer && (
                  <p className="text-xs text-text-muted mb-3 flex items-center gap-1.5">
                    <Building2 className="w-3.5 h-3.5 shrink-0 text-text-muted/60" />
                    <span className="truncate">{tender.customer}</span>
                  </p>
                )}

                {/* Meta chips */}
                <div className="flex flex-wrap items-center gap-2 mb-4">
                  {tender.amount > 0 && (
                    <span className="inline-flex items-center gap-1.5 text-xs px-2.5 py-1 bg-emerald-500/10 text-emerald-400 rounded-lg">
                      <Banknote className="w-3.5 h-3.5" />
                      {formatAmount(tender.amount)}
                    </span>
                  )}
                  {tender.lot_number && (
                    <span className="inline-flex items-center gap-1.5 text-xs px-2.5 py-1 bg-sky-500/10 text-sky-400 rounded-lg">
                      <Tag className="w-3.5 h-3.5" />
                      {tender.lot_number}
                    </span>
                  )}
                  {tender.method && (
                    <span className="inline-flex items-center gap-1.5 text-xs px-2.5 py-1 bg-purple-500/10 text-purple-400 rounded-lg max-w-[300px]">
                      <span className="truncate">{tender.method}</span>
                    </span>
                  )}
                </div>

                {/* Actions */}
                <div className="flex items-center gap-3">
                  {tender.url && (
                    <a
                      href={tender.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-1.5 text-xs font-medium text-primary hover:text-primary/80 transition-colors no-underline"
                    >
                      <ExternalLink className="w-3.5 h-3.5" />
                      Открыть на goszakup.gov.kz
                    </a>
                  )}
                </div>
              </div>
            ))}
          </div>

          {/* Pagination */}
          <div className="flex items-center justify-center gap-3 mt-8">
            {page > 1 && (
              <button
                onClick={() => doSearch(query, page - 1)}
                className="px-4 py-2 text-sm bg-surface-2 hover:bg-primary/15 border border-border hover:border-primary/30 rounded-xl transition-all"
              >
                Назад
              </button>
            )}
            <span className="text-sm text-text-muted">Страница {page}</span>
            {results.length >= 10 && (
              <button
                onClick={() => doSearch(query, page + 1)}
                className="px-4 py-2 text-sm bg-surface-2 hover:bg-primary/15 border border-border hover:border-primary/30 rounded-xl transition-all"
              >
                Далее
              </button>
            )}
          </div>
        </>
      ) : searched && !loading ? (
        <div className="text-center py-16">
          <SearchX className="w-12 h-12 text-text-muted/30 mx-auto mb-4" />
          <p className="text-text-muted text-sm">
            По запросу «{query}» ничего не найдено
          </p>
          <p className="text-text-muted/60 text-xs mt-1">
            Попробуйте изменить запрос или выберите категорию выше
          </p>
        </div>
      ) : (
        <div className="text-center py-16">
          <Sparkles className="w-12 h-12 text-primary/20 mx-auto mb-4" />
          <p className="text-text-muted text-sm">
            Введите запрос или выберите категорию для поиска тендеров
          </p>
        </div>
      )}
    </div>
  );
}

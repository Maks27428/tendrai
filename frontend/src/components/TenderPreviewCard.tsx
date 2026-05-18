import { useNavigate } from 'react-router-dom';
import type { TenderListItem } from '../api/client';
import { Building2, Banknote, ClipboardList, Calendar } from 'lucide-react';

interface Props {
  tender: TenderListItem;
}

function RiskBadge({ score }: { score: number }) {
  const color =
    score <= 30
      ? 'text-success border-success/40 bg-success/10'
      : score <= 60
      ? 'text-warning border-warning/40 bg-warning/10'
      : 'text-danger border-danger/40 bg-danger/10';
  const label = score <= 30 ? 'Низкий' : score <= 60 ? 'Средний' : 'Высокий';

  return (
    <span className={`inline-flex items-center gap-1.5 text-xs font-semibold px-2.5 py-1 rounded-full border ${color}`}>
      <span
        className={`w-1.5 h-1.5 rounded-full ${
          score <= 30 ? 'bg-success' : score <= 60 ? 'bg-warning' : 'bg-danger'
        }`}
      />
      Риск: {label}
    </span>
  );
}

export default function TenderPreviewCard({ tender }: Props) {
  const navigate = useNavigate();

  const amount = tender.summary?.amount ?? null;
  const customer = tender.summary?.customer ?? null;
  const reqCount = tender.requirements_count ?? null;

  const date = new Date(tender.created_at).toLocaleDateString('ru-RU', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  });

  return (
    <button
      onClick={() => navigate(`/analysis/${tender.id}`)}
      className="group w-full text-left bg-surface-2 border border-border rounded-2xl p-5
        hover:border-primary/50 hover:bg-surface-3/60 hover:shadow-lg hover:shadow-primary/5
        transition-all duration-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-primary"
    >
      {/* Title */}
      <p className="text-sm font-semibold text-text line-clamp-2 leading-snug mb-3 group-hover:text-primary transition-colors duration-200">
        {tender.title || 'Без названия'}
      </p>

      {/* Meta row */}
      <div className="flex flex-col gap-1.5 mb-4">
        {customer && (
          <div className="flex items-center gap-2 text-xs text-text-muted">
            <Building2 className="w-3.5 h-3.5 shrink-0" />
            <span className="truncate">{customer}</span>
          </div>
        )}
        {amount && (
          <div className="flex items-center gap-2 text-xs text-text-muted">
            <Banknote className="w-3.5 h-3.5 shrink-0" />
            <span className="truncate">{amount}</span>
          </div>
        )}
        {reqCount !== null && (
          <div className="flex items-center gap-2 text-xs text-text-muted">
            <ClipboardList className="w-3.5 h-3.5 shrink-0" />
            <span>{reqCount} требований</span>
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="flex items-center justify-between gap-2">
        {tender.risk_score !== null ? (
          <RiskBadge score={tender.risk_score} />
        ) : (
          <span />
        )}
        <div className="flex items-center gap-1 text-xs text-text-muted">
          <Calendar className="w-3 h-3" />
          {date}
        </div>
      </div>
    </button>
  );
}

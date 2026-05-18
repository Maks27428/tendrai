import type { RequirementData } from '../api/client';
import { CheckCircle2, AlertTriangle, XCircle, HelpCircle } from 'lucide-react';

interface Props {
  requirements: RequirementData[];
}

const STATUS_CONFIG = {
  ok: { icon: CheckCircle2, color: 'text-success', bg: 'bg-success/10', label: 'OK' },
  warning: { icon: AlertTriangle, color: 'text-warning', bg: 'bg-warning/10', label: 'Внимание' },
  critical: { icon: XCircle, color: 'text-danger', bg: 'bg-danger/10', label: 'Критично' },
  needs_review: { icon: HelpCircle, color: 'text-text-muted', bg: 'bg-surface-3', label: 'Проверить' },
};

const CATEGORY_LABELS: Record<string, string> = {
  qualification: 'Квалификация',
  technical: 'Технические',
  financial: 'Финансовые',
  deadline: 'Сроки',
  document: 'Документы',
};

export default function Checklist({ requirements }: Props) {
  if (!requirements.length) return null;

  const grouped = requirements.reduce<Record<string, RequirementData[]>>((acc, req) => {
    const cat = req.category || 'technical';
    if (!acc[cat]) acc[cat] = [];
    acc[cat].push(req);
    return acc;
  }, {});

  const stats = {
    critical: requirements.filter((r) => r.status === 'critical').length,
    warning: requirements.filter((r) => r.status === 'warning').length,
    ok: requirements.filter((r) => r.status === 'ok').length,
    total: requirements.length,
  };

  return (
    <div className="bg-surface-2 border border-border rounded-2xl p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-sm font-medium text-text-muted">
          Требования ({stats.total})
        </h3>
        <div className="flex gap-3 text-xs">
          <span className="text-danger">{stats.critical} крит.</span>
          <span className="text-warning">{stats.warning} вним.</span>
          <span className="text-success">{stats.ok} ок</span>
        </div>
      </div>

      <div className="space-y-4">
        {Object.entries(grouped).map(([category, reqs]) => (
          <div key={category}>
            <h4 className="text-xs font-medium text-text-muted uppercase tracking-wider mb-2">
              {CATEGORY_LABELS[category] || category}
            </h4>
            <div className="space-y-2">
              {reqs.map((req) => {
                const cfg = STATUS_CONFIG[req.status as keyof typeof STATUS_CONFIG] || STATUS_CONFIG.needs_review;
                const Icon = cfg.icon;
                return (
                  <div
                    key={req.id}
                    className={`flex items-start gap-3 p-3 rounded-lg ${cfg.bg}`}
                  >
                    <Icon className={`w-4 h-4 mt-0.5 shrink-0 ${cfg.color}`} />
                    <div className="flex-1 min-w-0">
                      <p className="text-sm text-text">{req.text}</p>
                      {req.details && (
                        <p className="text-xs text-text-muted mt-1">{req.details}</p>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

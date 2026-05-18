import type { Pitfall } from '../api/client';
import { AlertTriangle } from 'lucide-react';

interface Props {
  pitfalls: Pitfall[] | null;
}

const SEVERITY_STYLES = {
  high: 'border-danger/30 bg-danger/5',
  medium: 'border-warning/30 bg-warning/5',
  low: 'border-text-muted/20 bg-surface-3',
};

export default function Pitfalls({ pitfalls }: Props) {
  if (!pitfalls?.length) return null;

  return (
    <div className="bg-surface-2 border border-border rounded-2xl p-6">
      <h3 className="text-sm font-medium text-text-muted mb-4 flex items-center gap-2">
        <AlertTriangle className="w-4 h-4 text-warning" />
        Подводные камни ({pitfalls.length})
      </h3>
      <div className="space-y-3">
        {pitfalls.map((p, i) => {
          const style = SEVERITY_STYLES[p.severity as keyof typeof SEVERITY_STYLES] || SEVERITY_STYLES.medium;
          return (
            <div key={i} className={`border rounded-lg p-4 ${style}`}>
              <p className="text-sm text-text font-medium">{p.text}</p>
              {p.recommendation && (
                <p className="text-xs text-text-muted mt-2">
                  Рекомендация: {p.recommendation}
                </p>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}

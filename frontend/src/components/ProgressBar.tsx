import type { StreamEvent } from '../api/client';
import { Loader2, FileText, Brain, Shield, Sparkles, CheckCircle2, XCircle } from 'lucide-react';

const STAGES = [
  { key: 'parsing', label: 'Парсинг PDF', icon: FileText },
  { key: 'extracting', label: 'Извлечение требований', icon: Brain },
  { key: 'scoring', label: 'Оценка рисков', icon: Shield },
  { key: 'generating', label: 'Генерация предложения', icon: Sparkles },
];

interface Props {
  event: StreamEvent | null;
}

export default function ProgressBar({ event }: Props) {
  if (!event) return null;

  const currentIdx = STAGES.findIndex((s) => s.key === event.status);
  const isFailed = event.status === 'failed';
  const isCompleted = event.status === 'completed';

  return (
    <div className="bg-surface-2 border border-border rounded-2xl p-6">
      <div className="flex items-center gap-3 mb-6">
        {isFailed ? (
          <XCircle className="w-5 h-5 text-danger" />
        ) : isCompleted ? (
          <CheckCircle2 className="w-5 h-5 text-success" />
        ) : (
          <Loader2 className="w-5 h-5 text-primary animate-spin" />
        )}
        <span className="text-sm text-text-muted">
          {event.message || event.status}
        </span>
      </div>

      <div className="flex gap-2">
        {STAGES.map((stage, idx) => {
          const Icon = stage.icon;
          const isDone = isCompleted || idx < currentIdx;
          const isActive = idx === currentIdx && !isCompleted && !isFailed;

          return (
            <div key={stage.key} className="flex-1">
              <div
                className={`
                  h-2 rounded-full transition-all duration-500
                  ${isDone ? 'bg-success' : isActive ? 'bg-primary animate-pulse' : 'bg-surface-3'}
                `}
              />
              <div className="flex items-center gap-1.5 mt-2">
                <Icon className={`w-3.5 h-3.5 ${isDone ? 'text-success' : isActive ? 'text-primary' : 'text-text-muted'}`} />
                <span className={`text-xs ${isDone ? 'text-success' : isActive ? 'text-primary' : 'text-text-muted'}`}>
                  {stage.label}
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

import { useEffect, useState } from 'react';

interface Props {
  score: number | null;
  explanation: string;
}

export default function RiskScore({ score, explanation }: Props) {
  const [animated, setAnimated] = useState(false);

  useEffect(() => {
    if (score === null) return;
    // Tiny delay so the browser paints the initial state first
    const id = setTimeout(() => setAnimated(true), 50);
    return () => clearTimeout(id);
  }, [score]);

  if (score === null) return null;

  const color =
    score <= 30 ? 'text-success' : score <= 60 ? 'text-warning' : 'text-danger';
  const strokeColor =
    score <= 30 ? 'stroke-success' : score <= 60 ? 'stroke-warning' : 'stroke-danger';
  const label =
    score <= 30 ? 'Низкий риск' : score <= 60 ? 'Средний риск' : 'Высокий риск';

  const radius = 60;
  const circumference = 2 * Math.PI * radius;
  const targetOffset = circumference - (score / 100) * circumference;
  // Start fully undrawn, animate to the real offset
  const currentOffset = animated ? targetOffset : circumference;

  return (
    <div className="bg-surface-2 border border-border rounded-2xl p-6 flex flex-col items-center">
      <h3 className="text-sm font-medium text-text-muted mb-4">Оценка риска</h3>

      <div className="relative w-40 h-40">
        <svg className="w-full h-full -rotate-90" viewBox="0 0 140 140">
          {/* Track */}
          <circle
            cx="70" cy="70" r={radius}
            fill="none" strokeWidth="10"
            className="stroke-surface-3"
          />
          {/* Animated arc */}
          <circle
            cx="70" cy="70" r={radius}
            fill="none" strokeWidth="10"
            strokeLinecap="round"
            className={strokeColor}
            strokeDasharray={circumference}
            strokeDashoffset={currentOffset}
            style={{ transition: 'stroke-dashoffset 1.5s cubic-bezier(0.4, 0, 0.2, 1)' }}
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className={`text-3xl font-bold ${color}`}>{score}</span>
          <span className="text-xs text-text-muted">/100</span>
        </div>
      </div>

      <span className={`text-sm font-medium mt-2 ${color}`}>{label}</span>
      {explanation && (
        <p className="text-xs text-text-muted mt-3 text-center leading-relaxed">
          {explanation}
        </p>
      )}
    </div>
  );
}

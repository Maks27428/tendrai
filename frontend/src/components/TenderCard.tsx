import type { TenderSummary } from '../api/client';
import { Building2, Calendar, MapPin, Tag, Banknote } from 'lucide-react';

interface Props {
  title: string;
  summary: TenderSummary | null;
  pageCount: number | null;
}

export default function TenderCard({ title, summary, pageCount }: Props) {
  if (!summary) return null;

  const items = [
    { icon: Building2, label: 'Заказчик', value: summary.customer },
    { icon: Banknote, label: 'Сумма', value: summary.amount },
    { icon: Calendar, label: 'Дедлайн', value: summary.deadline },
    { icon: Tag, label: 'Категория', value: summary.category },
    { icon: MapPin, label: 'Место', value: summary.delivery_location },
  ];

  return (
    <div className="bg-surface-2 border border-border rounded-2xl p-6">
      <h2 className="text-lg font-semibold text-text mb-4 leading-snug">{title}</h2>
      {pageCount && (
        <span className="text-xs text-text-muted bg-surface-3 px-2 py-1 rounded-md">
          {pageCount} стр.
        </span>
      )}
      <div className="grid grid-cols-2 gap-4 mt-4">
        {items.map(({ icon: Icon, label, value }) =>
          value ? (
            <div key={label} className="flex items-start gap-2">
              <Icon className="w-4 h-4 text-text-muted mt-0.5 shrink-0" />
              <div>
                <p className="text-xs text-text-muted">{label}</p>
                <p className="text-sm text-text">{value}</p>
              </div>
            </div>
          ) : null,
        )}
      </div>
    </div>
  );
}

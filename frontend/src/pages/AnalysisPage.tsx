import { useEffect, useState } from 'react';
import type { ReactNode } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getTender } from '../api/client';
import type { TenderDetail } from '../api/client';
import { useSSE } from '../hooks/useSSE';
import ProgressBar from '../components/ProgressBar';
import TenderCard from '../components/TenderCard';
import RiskScore from '../components/RiskScore';
import Checklist from '../components/Checklist';
import Pitfalls from '../components/Pitfalls';
import Proposal from '../components/Proposal';
import { ArrowLeft } from 'lucide-react';

// Simple staggered fade-in: each block fades in with an increasing delay.
function FadeIn({
  children,
  delay = 0,
}: {
  children: ReactNode;
  delay?: number;
}) {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const id = setTimeout(() => setVisible(true), delay);
    return () => clearTimeout(id);
  }, [delay]);

  return (
    <div
      style={{
        opacity: visible ? 1 : 0,
        transform: visible ? 'translateY(0)' : 'translateY(12px)',
        transition: 'opacity 0.4s ease, transform 0.4s ease',
      }}
    >
      {children}
    </div>
  );
}

export default function AnalysisPage() {
  const { id } = useParams<{ id: string }>();
  const tenderId = id ? parseInt(id, 10) : null;
  const [tender, setTender] = useState<TenderDetail | null>(null);
  const [loading, setLoading] = useState(true);

  const isProcessing = tender
    ? !['completed', 'failed'].includes(tender.status)
    : false;

  const { event, done } = useSSE(isProcessing ? tenderId : null);

  useEffect(() => {
    if (!tenderId) return;
    getTender(tenderId)
      .then((data) => {
        setTender(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [tenderId]);

  useEffect(() => {
    if (done && tenderId) {
      getTender(tenderId).then(setTender);
    }
  }, [done, tenderId]);

  // Periodic refresh while processing
  useEffect(() => {
    if (!isProcessing || !tenderId) return;
    const interval = setInterval(() => {
      getTender(tenderId).then(setTender);
    }, 2000);
    return () => clearInterval(interval);
  }, [isProcessing, tenderId]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="w-10 h-10 border-4 border-primary border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  if (!tender) {
    return (
      <div className="text-center py-16">
        <p className="text-text-muted">Тендер не найден</p>
        <Link to="/" className="text-primary hover:underline text-sm mt-2 inline-block">
          Вернуться на главную
        </Link>
      </div>
    );
  }

  return (
    <div>
      <FadeIn delay={0}>
        <Link
          to="/"
          className="inline-flex items-center gap-2 text-sm text-text-muted hover:text-text mb-6 no-underline"
        >
          <ArrowLeft className="w-4 h-4" />
          Назад
        </Link>
      </FadeIn>

      {isProcessing && (
        <FadeIn delay={50}>
          <ProgressBar event={event} />
        </FadeIn>
      )}

      {tender.status === 'failed' && (
        <FadeIn delay={100}>
          <div className="bg-danger/10 border border-danger/30 rounded-2xl p-6 mb-6">
            <p className="text-danger text-sm">{tender.progress_message}</p>
          </div>
        </FadeIn>
      )}

      {(tender.summary || tender.status === 'completed') && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-6">
          <div className="lg:col-span-2 space-y-6">
            <FadeIn delay={100}>
              <TenderCard
                title={tender.title}
                summary={tender.summary}
                pageCount={tender.page_count}
              />
            </FadeIn>
            <FadeIn delay={200}>
              <Checklist requirements={tender.requirements} />
            </FadeIn>
            <FadeIn delay={300}>
              <Proposal proposal={tender.technical_proposal} />
            </FadeIn>
          </div>
          <div className="space-y-6">
            <FadeIn delay={150}>
              <RiskScore
                score={tender.risk_score}
                explanation={tender.risk_explanation}
              />
            </FadeIn>
            <FadeIn delay={250}>
              <Pitfalls pitfalls={tender.pitfalls} />
            </FadeIn>
          </div>
        </div>
      )}
    </div>
  );
}

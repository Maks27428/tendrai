import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import UploadZone from '../components/UploadZone';
import TenderPreviewCard from '../components/TenderPreviewCard';
import { uploadTender, uploadDemoPdf, getDemoPdfs, getTenders } from '../api/client';
import type { TenderListItem, DemoPdf } from '../api/client';
import { AlertTriangle, Sparkles, Clock, Play, ExternalLink } from 'lucide-react';

export default function HomePage() {
  const navigate = useNavigate();
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState('');
  const [tenders, setTenders] = useState<TenderListItem[]>([]);
  const [loadingTenders, setLoadingTenders] = useState(true);
  const [demoPdfs, setDemoPdfs] = useState<DemoPdf[]>([]);
  const [loadingDemo, setLoadingDemo] = useState('');

  useEffect(() => {
    getTenders()
      .then(setTenders)
      .catch(() => {})
      .finally(() => setLoadingTenders(false));
    getDemoPdfs().then(setDemoPdfs).catch(() => {});
  }, []);

  const handleDemo = async (filename: string) => {
    setLoadingDemo(filename);
    setError('');
    try {
      const tender = await uploadDemoPdf(filename);
      navigate(`/analysis/${tender.id}`);
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : 'Ошибка загрузки демо';
      setError(msg);
      setLoadingDemo('');
    }
  };

  const handleUpload = async (file: File) => {
    setIsUploading(true);
    setError('');
    try {
      const tender = await uploadTender(file);
      navigate(`/analysis/${tender.id}`);
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : 'Ошибка загрузки';
      setError(msg);
      setIsUploading(false);
    }
  };

  const completedAll = tenders.filter((t) => t.status === 'completed');
  const seen = new Set<string>();
  const completed = completedAll.filter((t) => {
    const key = t.title || `untitled-${t.id}`;
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
  const inProgress = tenders.filter((t) => !['completed', 'failed'].includes(t.status));
  const hasTenders = tenders.length > 0;

  return (
    <div className="max-w-4xl mx-auto">
      {/* Hero */}
      <div className={`text-center ${hasTenders ? 'mb-6' : 'mb-10'}`}>
        <h1 className={`font-bold text-text mb-3 ${hasTenders ? 'text-3xl' : 'text-4xl'}`}>
          Анализ тендеров за минуты, а не дни
        </h1>
        <p className="text-text-muted text-lg">
          Загрузите PDF с goszakup.gov.kz — получите анализ требований, оценку рисков и черновик технического предложения
        </p>
      </div>

      {/* Upload zone — compact when tenders exist */}
      <div className={hasTenders ? '[&_>div]:p-8' : ''}>
        <UploadZone onUpload={handleUpload} isUploading={isUploading} />
      </div>

      {/* Demo PDFs + Instructions */}
      <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Demo button */}
        {demoPdfs.length > 0 && (
          <div className="p-5 bg-surface-2 border border-border rounded-xl">
            <h3 className="text-sm font-semibold text-text mb-3 flex items-center gap-2">
              <Play className="w-4 h-4 text-primary" />
              Попробовать на демо-PDF
            </h3>
            <div className="space-y-2">
              {demoPdfs.map((pdf) => (
                <button
                  key={pdf.filename}
                  onClick={() => handleDemo(pdf.filename)}
                  disabled={!!loadingDemo || isUploading}
                  className="w-full flex items-center gap-3 px-4 py-3 bg-primary/10 hover:bg-primary/20 border border-primary/30 rounded-lg transition-colors text-left disabled:opacity-50"
                >
                  {loadingDemo === pdf.filename ? (
                    <div className="w-4 h-4 border-2 border-primary border-t-transparent rounded-full animate-spin shrink-0" />
                  ) : (
                    <Play className="w-4 h-4 text-primary shrink-0" />
                  )}
                  <span className="text-sm text-text">{pdf.name}</span>
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Instructions */}
        <div className="p-5 bg-surface-2 border border-border rounded-xl">
          <h3 className="text-sm font-semibold text-text mb-3 flex items-center gap-2">
            <ExternalLink className="w-4 h-4 text-warning" />
            Загрузить свой тендер
          </h3>
          <ol className="space-y-2 text-sm text-text-muted">
            <li className="flex gap-2">
              <span className="text-primary font-bold">1.</span>
              <span>Откройте <a href="https://goszakup.gov.kz" target="_blank" rel="noopener noreferrer" className="text-primary hover:underline">goszakup.gov.kz</a></span>
            </li>
            <li className="flex gap-2">
              <span className="text-primary font-bold">2.</span>
              <span>Найдите интересующий тендер</span>
            </li>
            <li className="flex gap-2">
              <span className="text-primary font-bold">3.</span>
              <span>Скачайте PDF с техническим заданием</span>
            </li>
            <li className="flex gap-2">
              <span className="text-primary font-bold">4.</span>
              <span>Перетащите PDF в зону загрузки выше</span>
            </li>
          </ol>
        </div>
      </div>

      {error && (
        <div className="mt-4 p-4 bg-danger/10 border border-danger/30 rounded-xl flex items-center gap-3">
          <AlertTriangle className="w-5 h-5 text-danger shrink-0" />
          <p className="text-sm text-danger">{error}</p>
        </div>
      )}

      {/* In-progress tenders */}
      {inProgress.length > 0 && (
        <div className="mt-8">
          <h2 className="text-sm font-medium text-text-muted mb-3 flex items-center gap-2">
            <Clock className="w-4 h-4" />
            Обрабатываются
          </h2>
          <div className="space-y-2">
            {inProgress.map((t) => (
              <button
                key={t.id}
                onClick={() => navigate(`/analysis/${t.id}`)}
                className="w-full flex items-center gap-4 p-4 bg-surface-2 border border-border rounded-xl hover:border-primary/50 transition-colors text-left"
              >
                <div className="w-4 h-4 border-2 border-primary border-t-transparent rounded-full animate-spin shrink-0" />
                <p className="text-sm text-text truncate flex-1">
                  {t.title || 'Обработка…'}
                </p>
                <span className="text-xs px-2 py-1 rounded-md bg-primary/10 text-primary">
                  В процессе
                </span>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Completed demo analyses */}
      {loadingTenders ? null : completed.length > 0 ? (
        <div className="mt-10">
          <div className="flex items-center gap-2 mb-5">
            <Sparkles className="w-4 h-4 text-primary" />
            <h2 className="text-base font-semibold text-text">Готовые анализы</h2>
            <span className="ml-auto text-xs text-text-muted">
              {completed.length} {completed.length === 1 ? 'тендер' : completed.length < 5 ? 'тендера' : 'тендеров'}
            </span>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {completed.map((t) => (
              <TenderPreviewCard key={t.id} tender={t} />
            ))}
          </div>
        </div>
      ) : !loadingTenders && tenders.length === 0 ? (
        <div className="mt-10 text-center py-10 border border-dashed border-border rounded-2xl">
          <p className="text-text-muted text-sm">
            Загрузите первый тендер — результаты появятся здесь
          </p>
        </div>
      ) : null}
    </div>
  );
}

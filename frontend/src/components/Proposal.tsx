import { useState } from 'react';
import { ChevronDown, ChevronUp, Copy, Check } from 'lucide-react';

interface Props {
  proposal: string;
}

export default function Proposal({ proposal }: Props) {
  const [expanded, setExpanded] = useState(false);
  const [copied, setCopied] = useState(false);

  if (!proposal) return null;

  const handleCopy = async () => {
    await navigator.clipboard.writeText(proposal);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="bg-surface-2 border border-border rounded-2xl p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-sm font-medium text-text-muted">
          Техническое предложение (черновик)
        </h3>
        <div className="flex gap-2">
          <button
            onClick={handleCopy}
            className="flex items-center gap-1.5 text-xs px-3 py-1.5 rounded-lg bg-surface-3 text-text-muted hover:text-text transition-colors"
          >
            {copied ? <Check className="w-3.5 h-3.5" /> : <Copy className="w-3.5 h-3.5" />}
            {copied ? 'Скопировано' : 'Копировать'}
          </button>
          <button
            onClick={() => setExpanded(!expanded)}
            className="flex items-center gap-1.5 text-xs px-3 py-1.5 rounded-lg bg-surface-3 text-text-muted hover:text-text transition-colors"
          >
            {expanded ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
            {expanded ? 'Свернуть' : 'Развернуть'}
          </button>
        </div>
      </div>

      <div
        className={`prose prose-invert prose-sm max-w-none overflow-hidden transition-all duration-500 ${
          expanded ? 'max-h-none' : 'max-h-64'
        }`}
      >
        <div className="whitespace-pre-wrap text-sm text-text leading-relaxed">
          {proposal}
        </div>
      </div>

      {!expanded && (
        <div className="relative -mt-16 h-16 bg-gradient-to-t from-surface-2 to-transparent pointer-events-none" />
      )}
    </div>
  );
}

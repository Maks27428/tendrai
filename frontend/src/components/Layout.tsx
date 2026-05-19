import type { ReactNode } from 'react';
import { Link } from 'react-router-dom';
import { FileSearch, Shield } from 'lucide-react';

export default function Layout({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen flex flex-col">
      <header className="border-b border-border bg-surface-2 px-6 py-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <Link to="/" className="flex items-center gap-3 no-underline">
            <div className="w-10 h-10 bg-primary rounded-xl flex items-center justify-center">
              <FileSearch className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-text m-0">TendrAI</h1>
              <p className="text-xs text-text-muted m-0">AI-ассистент госзакупок</p>
            </div>
          </Link>
          <Link
            to="/monopoly"
            className="flex items-center gap-2 px-4 py-2 bg-warning/10 hover:bg-warning/20 border border-warning/30 rounded-lg transition-colors no-underline"
          >
            <Shield className="w-4 h-4 text-warning" />
            <span className="text-sm font-medium text-warning">Проверка на монополию</span>
          </Link>
        </div>
      </header>
      <main className="flex-1 max-w-7xl mx-auto w-full px-6 py-8">
        {children}
      </main>
    </div>
  );
}

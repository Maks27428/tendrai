import type { ReactNode } from 'react';
import { Link } from 'react-router-dom';
import { FileSearch, Shield, Search, LogIn, LogOut, User } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

export default function Layout({ children }: { children: ReactNode }) {
  const { user, logout } = useAuth();

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
          <div className="flex items-center gap-3">
            <Link
              to="/search"
              className="flex items-center gap-2 px-4 py-2 bg-primary/10 hover:bg-primary/20 border border-primary/30 rounded-lg transition-colors no-underline"
            >
              <Search className="w-4 h-4 text-primary" />
              <span className="text-sm font-medium text-primary">Найти тендер</span>
            </Link>
            <Link
              to="/monopoly"
              className="flex items-center gap-2 px-4 py-2 bg-warning/10 hover:bg-warning/20 border border-warning/30 rounded-lg transition-colors no-underline"
            >
              <Shield className="w-4 h-4 text-warning" />
              <span className="text-sm font-medium text-warning">Проверка на монополию</span>
            </Link>
            {user ? (
              <div className="flex items-center gap-2 ml-2">
                <span className="flex items-center gap-1.5 text-sm text-text">
                  <User className="w-4 h-4 text-primary" />
                  {user.nickname}
                </span>
                <button
                  onClick={logout}
                  className="flex items-center gap-1.5 px-3 py-2 text-sm text-text-muted hover:text-danger border border-border hover:border-danger/30 rounded-lg transition-colors"
                >
                  <LogOut className="w-4 h-4" />
                  Выйти
                </button>
              </div>
            ) : (
              <Link
                to="/login"
                className="flex items-center gap-2 px-4 py-2 bg-surface hover:bg-primary/10 border border-border hover:border-primary/30 rounded-lg transition-colors no-underline ml-2"
              >
                <LogIn className="w-4 h-4 text-text-muted" />
                <span className="text-sm font-medium text-text">Войти</span>
              </Link>
            )}
          </div>
        </div>
      </header>
      <main className="flex-1 max-w-7xl mx-auto w-full px-6 py-8">
        {children}
      </main>
    </div>
  );
}

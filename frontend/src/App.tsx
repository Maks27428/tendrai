import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import HomePage from './pages/HomePage';
import AnalysisPage from './pages/AnalysisPage';
import MonopolyPage from './pages/MonopolyPage';
import SearchPage from './pages/SearchPage';

export default function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/analysis/:id" element={<AnalysisPage />} />
          <Route path="/monopoly" element={<MonopolyPage />} />
          <Route path="/search" element={<SearchPage />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}

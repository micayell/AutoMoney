import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { useEffect } from 'react';
import { initGA, logPageView } from './utils/analytics';
import { Navbar } from './components/Navbar';
import { Dashboard } from './pages/Dashboard';
import { AssetPage } from './pages/AssetPage';
import { StockPage } from './pages/StockPage';
import { LottoPage } from './pages/LottoPage';
import './index.css';

const queryClient = new QueryClient();

function App() {
  useEffect(() => {
    initGA();
    logPageView();
  }, []);

  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <div className="min-h-screen bg-gray-50">
          <Navbar />
          <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/assets" element={<AssetPage />} />
              <Route path="/stock" element={<StockPage />} />
              <Route path="/lotto" element={<LottoPage />} />
            </Routes>
          </main>
        </div>
      </Router>
    </QueryClientProvider>
  );
}

export default App;

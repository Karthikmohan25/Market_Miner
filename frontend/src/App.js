import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import ChatSearchPage from './pages/ChatSearchPage';
import SearchPage from './pages/SearchPage';
import ResultsPage from './pages/ResultsPage';
import TrendsPage from './pages/TrendsPage';
import './styles/globals.css';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-900 text-white">
        <Routes>
          {/* New AI Chat Interface as default */}
          <Route path="/" element={<ChatSearchPage />} />
          
          {/* Original pages for comparison/fallback */}
          <Route path="/classic" element={
            <>
              <Header />
              <main className="container mx-auto px-4 py-8">
                <SearchPage />
              </main>
            </>
          } />
          <Route path="/results" element={
            <>
              <Header />
              <main className="container mx-auto px-4 py-8">
                <ResultsPage />
              </main>
            </>
          } />
          <Route path="/trends" element={
            <>
              <Header />
              <main className="container mx-auto px-4 py-8">
                <TrendsPage />
              </main>
            </>
          } />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
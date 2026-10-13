import { useState } from 'react';
import ArchitectureView from './components/ArchitectureView';
import RoadmapView from './components/RoadmapView';
import ComplianceView from './components/ComplianceView';
import OverviewView from './components/OverviewView';
import DataFlowView from './components/DataFlowView';
import MetricsView from './components/MetricsView';
import DependencyView from './components/DependencyView';
import SecurityView from './components/SecurityView';
import InstallationView from './components/InstallationView';

type Tab = 'overview' | 'architecture' | 'roadmap' | 'dataflow' | 'dependencies' | 'metrics' | 'security' | 'installation' | 'compliance';

function App() {
  const [activeTab, setActiveTab] = useState<Tab>('overview');

  const tabs: { id: Tab; label: string; icon: string }[] = [
    { id: 'overview', label: 'Обзор', icon: '🏠' },
    { id: 'architecture', label: 'Архитектура', icon: '🧠' },
    { id: 'dataflow', label: 'Поток данных', icon: '🔄' },
    { id: 'roadmap', label: 'Дорожная карта', icon: '🗺️' },
    { id: 'dependencies', label: 'Зависимости', icon: '🕸️' },
    { id: 'security', label: 'Безопасность', icon: '🔐' },
    { id: 'metrics', label: 'Метрики', icon: '📊' },
    { id: 'installation', label: 'Установка', icon: '📦' },
    { id: 'compliance', label: 'Соответствие', icon: '✅' },
  ];

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">
      {/* Header */}
      <header className="border-b border-gray-800 bg-gray-950/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-xl shadow-lg shadow-blue-500/20">
                🤖
              </div>
              <div>
                <h1 className="text-xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                  Джарвис — AI Ассистент
                </h1>
                <p className="text-xs text-gray-500">Архитектура • План • Метрики • Контроль</p>
              </div>
            </div>
            <div className="hidden md:flex items-center gap-2 text-xs text-gray-500">
              <span className="inline-flex items-center gap-1 px-2 py-1 rounded-full bg-green-900/30 text-green-400 border border-green-800">
                <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
                Планирование
              </span>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation */}
      <nav className="border-b border-gray-800 bg-gray-900/50">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex gap-1 overflow-x-auto scrollbar-hide">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-4 py-3 text-sm font-medium whitespace-nowrap transition-all border-b-2 ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-400'
                    : 'border-transparent text-gray-400 hover:text-gray-200 hover:border-gray-600'
                }`}
              >
                <span className="mr-2">{tab.icon}</span>
                {tab.label}
              </button>
            ))}
          </div>
        </div>
      </nav>

      {/* Content */}
      <main className="max-w-7xl mx-auto px-4 py-6">
        {activeTab === 'overview' && <OverviewView onNavigate={setActiveTab} />}
        {activeTab === 'architecture' && <ArchitectureView />}
        {activeTab === 'dataflow' && <DataFlowView />}
        {activeTab === 'roadmap' && <RoadmapView />}
        {activeTab === 'dependencies' && <DependencyView />}
        {activeTab === 'security' && <SecurityView />}
        {activeTab === 'metrics' && <MetricsView />}
        {activeTab === 'installation' && <InstallationView />}
        {activeTab === 'compliance' && <ComplianceView />}
      </main>

      {/* Footer */}
      <footer className="border-t border-gray-800 mt-12">
        <div className="max-w-7xl mx-auto px-4 py-6 text-center text-xs text-gray-600">
          <p>🤖 Джарвис AI — Голосовой ассистент нового поколения</p>
          <p className="mt-1">Python • asyncio • llama-cpp • faster-whisper • PyQt6 • SQLite • WebRTC</p>
        </div>
      </footer>
    </div>
  );
}

export default App;

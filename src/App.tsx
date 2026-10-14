import { useState } from 'react';
import JarvisInterface from './components/JarvisInterface';
import ArchitectureView from './components/ArchitectureView';
import RoadmapView from './components/RoadmapView';
import ComplianceView from './components/ComplianceView';
import OverviewView from './components/OverviewView';
import DataFlowView from './components/DataFlowView';
import MetricsView from './components/MetricsView';
import DependencyView from './components/DependencyView';
import SecurityView from './components/SecurityView';
import InstallationView from './components/InstallationView';
import BuildProgressView from './components/BuildProgressView';
import { LayoutDashboard, Monitor } from 'lucide-react';

type Tab = 'jarvis' | 'overview' | 'architecture' | 'roadmap' | 'dataflow' | 'dependencies' | 'metrics' | 'security' | 'installation' | 'build' | 'compliance';

function App() {
  const [activeTab, setActiveTab] = useState<Tab>('jarvis');
  const [showDashboard, setShowDashboard] = useState(false);

  const tabs = [
    { id: 'jarvis' as Tab, label: 'Джарвис', icon: '🤖' },
    { id: 'overview' as Tab, label: 'Обзор', icon: '🏠' },
    { id: 'architecture' as Tab, label: 'Архитектура', icon: '🧠' },
    { id: 'dataflow' as Tab, label: 'Поток данных', icon: '🔄' },
    { id: 'roadmap' as Tab, label: 'Дорожная карта', icon: '🗺️' },
    { id: 'build' as Tab, label: 'Сборка', icon: '🏗️' },
    { id: 'dependencies' as Tab, label: 'Зависимости', icon: '🕸️' },
    { id: 'security' as Tab, label: 'Безопасность', icon: '🔐' },
    { id: 'metrics' as Tab, label: 'Метрики', icon: '📊' },
    { id: 'installation' as Tab, label: 'Установка', icon: '📦' },
    { id: 'compliance' as Tab, label: 'Соответствие', icon: '✅' },
  ];

  // Если выбран Джарвис, показываем полный интерфейс
  if (activeTab === 'jarvis') {
    return (
      <div className="relative">
        <JarvisInterface />
        <button
          onClick={() => setActiveTab('overview')}
          className="fixed bottom-6 right-6 z-50 px-4 py-2 bg-white/10 backdrop-blur-xl rounded-full border border-white/20 hover:bg-white/20 transition-all flex items-center gap-2 text-sm"
        >
          <LayoutDashboard className="w-4 h-4" />
          Панель управления
        </button>
      </div>
    );
  }

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
            <div className="flex items-center gap-3">
              <button
                onClick={() => setActiveTab('jarvis')}
                className="px-4 py-2 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 rounded-lg font-medium transition-all text-sm flex items-center gap-2 shadow-lg shadow-blue-500/20"
              >
                <Monitor className="w-4 h-4" />
                Интерфейс
              </button>
              <span className="hidden md:inline-flex items-center gap-1 px-2 py-1 rounded-full bg-green-900/30 text-green-400 border border-green-800">
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
            {tabs.filter(t => t.id !== 'jarvis').map((tab) => (
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
        {activeTab === 'build' && <BuildProgressView />}
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

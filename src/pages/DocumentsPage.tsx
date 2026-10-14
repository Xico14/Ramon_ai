import { useState } from 'react';
import { motion } from 'framer-motion';
import { Upload, FileText, Trash2, Search } from 'lucide-react';
import { useAppStore } from '../store';
import { cn } from '../lib/utils';
import type { Document } from '../types';

export function DocumentsPage() {
  const { documents, addDocument, removeDocument } = useAppStore();
  const [searchQuery, setSearchQuery] = useState('');

  const handleUpload = () => {
    // Симуляция загрузки документа
    const newDoc: Document = {
      id: Date.now().toString(),
      title: `Документ ${documents.length + 1}`,
      source: 'upload',
      format: 'pdf',
      size: Math.floor(Math.random() * 1000000),
      chunks: Math.floor(Math.random() * 50) + 10,
      uploadedAt: new Date(),
    };
    addDocument(newDoc);
  };

  const filteredDocs = documents.filter(doc =>
    doc.title.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between"
      >
        <div>
          <h1 className="text-3xl font-bold text-white mb-2">Документы</h1>
          <p className="text-gray-400">Управление документами для RAG</p>
        </div>
        <button
          onClick={handleUpload}
          className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors flex items-center gap-2"
        >
          <Upload className="w-4 h-4" />
          Загрузить
        </button>
      </motion.div>

      {/* Search */}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Поиск документов..."
          className="w-full bg-gray-900 border border-gray-800 rounded-lg pl-10 pr-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/50"
        />
      </div>

      {/* Documents Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredDocs.length === 0 ? (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="col-span-full text-center py-12"
          >
            <FileText className="w-16 h-16 text-gray-600 mx-auto mb-4" />
            <p className="text-gray-400">Нет документов</p>
            <p className="text-sm text-gray-500">Загрузите документы для поиска</p>
          </motion.div>
        ) : (
          filteredDocs.map((doc, index) => (
            <motion.div
              key={doc.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.05 }}
              className="bg-gray-900 border border-gray-800 rounded-xl p-4 hover:border-gray-700 transition-all"
            >
              <div className="flex items-start justify-between mb-3">
                <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-purple-500 to-pink-600 flex items-center justify-center">
                  <FileText className="w-5 h-5 text-white" />
                </div>
                <button
                  onClick={() => removeDocument(doc.id)}
                  className="p-1 rounded-lg hover:bg-gray-800 text-gray-400 hover:text-red-500 transition-colors"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
              <h3 className="font-semibold text-white mb-1 truncate">{doc.title}</h3>
              <div className="space-y-1 text-xs text-gray-400">
                <div>Формат: {doc.format.toUpperCase()}</div>
                <div>Размер: {(doc.size / 1024).toFixed(1)} KB</div>
                <div>Чанков: {doc.chunks}</div>
                <div>Загружен: {new Date(doc.uploadedAt).toLocaleDateString('ru-RU')}</div>
              </div>
            </motion.div>
          ))
        )}
      </div>
    </div>
  );
}

export interface Tool {
  id: string;
  name: string;
  description: string;
  scope: string;
  risk: 'low' | 'medium' | 'high';
  requiresConfirmation: boolean;
  example: string;
}

export const tools: Tool[] = [
  {
    id: 'calculator',
    name: 'Калькулятор',
    description: 'Математические вычисления',
    scope: 'math',
    risk: 'low',
    requiresConfirmation: false,
    example: '{"action": "calculate", "expression": "2+2*2"}',
  },
  {
    id: 'search',
    name: 'Поиск в интернете',
    description: 'Поиск информации (локальный/онлайн)',
    scope: 'web',
    risk: 'low',
    requiresConfirmation: false,
    example: '{"action": "search", "query": "погода Москва"}',
  },
  {
    id: 'notepad',
    name: 'Блокнот',
    description: 'Читать/писать заметки',
    scope: 'files.local',
    risk: 'low',
    requiresConfirmation: false,
    example: '{"action": "write", "path": "~/notes.txt", "content": "..."}',
  },
  {
    id: 'open_app',
    name: 'Открыть приложение',
    description: 'Запуск программ на компьютере',
    scope: 'system.apps',
    risk: 'medium',
    requiresConfirmation: true,
    example: '{"action": "open", "app": "notepad.exe"}',
  },
  {
    id: 'file_ops',
    name: 'Файловые операции',
    description: 'Копирование, перемещение файлов',
    scope: 'files.system',
    risk: 'medium',
    requiresConfirmation: true,
    example: '{"action": "copy", "from": "a.txt", "to": "b.txt"}',
  },
  {
    id: 'delete',
    name: 'Удаление файлов',
    description: 'Удаление файлов и папок',
    scope: 'files.dangerous',
    risk: 'high',
    requiresConfirmation: true,
    example: '{"action": "delete", "path": "file.txt"}',
  },
  {
    id: 'send_email',
    name: 'Отправить email',
    description: 'Отправка писем от имени пользователя',
    scope: 'network.email',
    risk: 'high',
    requiresConfirmation: true,
    example: '{"action": "send", "to": "user@mail.com", "subject": "..."}',
  },
  {
    id: 'system_cmd',
    name: 'Системные команды',
    description: 'Выполнение команд ОС',
    scope: 'system.dangerous',
    risk: 'high',
    requiresConfirmation: true,
    example: '{"action": "exec", "command": "dir"}',
  },
];

export default function SecurityView() {
  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'low': return 'text-green-400 bg-green-900/30 border-green-800';
      case 'medium': return 'text-yellow-400 bg-yellow-900/30 border-yellow-800';
      case 'high': return 'text-red-400 bg-red-900/30 border-red-800';
      default: return 'text-gray-400 bg-gray-900/30 border-gray-800';
    }
  };

  const getRiskLabel = (risk: string) => {
    switch (risk) {
      case 'low': return 'Низкий';
      case 'medium': return 'Средний';
      case 'high': return 'Высокий';
      default: return '';
    }
  };

  return (
    <div className="space-y-6">
      {/* Title */}
      <div>
        <h2 className="text-2xl font-bold mb-2">🔐 Безопасность и Инструменты (MCP)</h2>
        <p className="text-gray-400 text-sm">
          Model Context Protocol — как робот вызывает инструменты с контролем безопасности.
        </p>
      </div>

      {/* MCP Flow */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
        <h3 className="font-bold mb-4">🔄 Поток вызова инструмента</h3>
        <div className="flex flex-wrap items-center gap-2 justify-center">
          {[
            { label: 'LLM решает', sub: 'Нужен инструмент', icon: '🧠', color: 'bg-purple-800' },
            { label: 'Генерирует JSON', sub: 'GBNF формат', icon: '📝', color: 'bg-blue-800' },
            { label: 'Orchestrator', sub: 'Проверяет scope', icon: '🔍', color: 'bg-cyan-800' },
            { label: 'Risk check', sub: 'Оценка риска', icon: '⚠️', color: 'bg-yellow-800' },
            { label: 'Confirmation?', sub: 'Спрашивает юзера', icon: '❓', color: 'bg-orange-800' },
            { label: 'Execute', sub: 'Выполняет', icon: '✅', color: 'bg-green-800' },
            { label: 'Audit log', sub: 'Записывает', icon: '📋', color: 'bg-gray-700' },
          ].map((step, i) => (
            <div key={i} className="flex items-center gap-2">
              <div className={`${step.color} rounded-lg px-3 py-2 text-center min-w-[80px]`}>
                <div className="text-lg">{step.icon}</div>
                <div className="text-[10px] font-bold">{step.label}</div>
                <div className="text-[8px] opacity-70">{step.sub}</div>
              </div>
              {i < 6 && <span className="text-gray-600">→</span>}
            </div>
          ))}
        </div>
      </div>

      {/* Scopes */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
        <h3 className="font-bold mb-4">🏷️ Система скоупов (разрешений)</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {[
            { scope: 'math', label: 'Математика', icon: '🔢', level: 'Без ограничений' },
            { scope: 'web', label: 'Интернет', icon: '🌐', level: 'Без ограничений' },
            { scope: 'files.local', label: 'Локальные файлы', icon: '📁', level: 'Только ~/jarvis/' },
            { scope: 'files.system', label: 'Системные файлы', icon: '💾', level: 'Требует подтверждения' },
            { scope: 'files.dangerous', label: 'Удаление', icon: '🗑️', level: 'Двойное подтверждение' },
            { scope: 'system.apps', label: 'Приложения', icon: '🖥️', level: 'Требует подтверждения' },
            { scope: 'system.dangerous', label: 'Команды ОС', icon: '⚡', level: 'Только whitelist' },
            { scope: 'network.email', label: 'Email', icon: '📧', level: 'Всегда подтверждение' },
          ].map((s) => (
            <div key={s.scope} className="bg-gray-800/50 border border-gray-700 rounded-lg p-3">
              <div className="text-lg mb-1">{s.icon}</div>
              <div className="text-xs font-bold">{s.label}</div>
              <div className="text-[10px] text-gray-500 font-mono mt-1">{s.scope}</div>
              <div className="text-[10px] text-yellow-400 mt-1">{s.level}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Tools Grid */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
        <h3 className="font-bold mb-4">🛠️ Доступные инструменты</h3>
        <div className="grid md:grid-cols-2 gap-3">
          {tools.map((tool) => (
            <div key={tool.id} className="bg-gray-800/30 border border-gray-700 rounded-lg p-4 hover:border-gray-600 transition-colors">
              <div className="flex items-center justify-between mb-2">
                <h4 className="font-bold text-sm">{tool.name}</h4>
                <div className="flex items-center gap-2">
                  <span className={`text-[10px] px-1.5 py-0.5 rounded border ${getRiskColor(tool.risk)}`}>
                    {getRiskLabel(tool.risk)}
                  </span>
                  {tool.requiresConfirmation && (
                    <span className="text-[10px] px-1.5 py-0.5 rounded bg-orange-900/30 text-orange-400 border border-orange-800">
                      ⚠️ Подтверждение
                    </span>
                  )}
                </div>
              </div>
              <p className="text-xs text-gray-400 mb-2">{tool.description}</p>
              <div className="bg-black/40 rounded p-2">
                <code className="text-[10px] text-green-300 font-mono break-all">{tool.example}</code>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Security Layers */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
        <h3 className="font-bold mb-4">🛡️ Слои безопасности</h3>
        <div className="space-y-3">
          {[
            {
              layer: '1. GBNF Grammar',
              desc: 'LLM физически не может сгенерировать невалидный JSON',
              icon: '📐',
              color: 'border-purple-700 bg-purple-900/20',
            },
            {
              layer: '2. Scope Check',
              desc: 'Orchestrator проверяет, есть ли разрешение на операцию',
              icon: '🔍',
              color: 'border-blue-700 bg-blue-900/20',
            },
            {
              layer: '3. Risk Assessment',
              desc: 'Оценка риска: low/medium/high. High всегда требует подтверждения',
              icon: '⚠️',
              color: 'border-yellow-700 bg-yellow-900/20',
            },
            {
              layer: '4. User Confirmation',
              desc: '"Ты уверен, что хочешь удалить файл?" — ждём ответ',
              icon: '❓',
              color: 'border-orange-700 bg-orange-900/20',
            },
            {
              layer: '5. Audit Log',
              desc: 'Все действия записываются в SQLite для разбора',
              icon: '📋',
              color: 'border-green-700 bg-green-900/20',
            },
            {
              layer: '6. Encryption (AES-GCM)',
              desc: 'Настройки, ключи API, токены — зашифрованы на диске',
              icon: '🔐',
              color: 'border-red-700 bg-red-900/20',
            },
          ].map((item) => (
            <div key={item.layer} className={`${item.color} border rounded-lg p-3 flex items-start gap-3`}>
              <span className="text-xl">{item.icon}</span>
              <div>
                <div className="text-sm font-bold">{item.layer}</div>
                <div className="text-xs text-gray-400">{item.desc}</div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Update/Backup */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
        <h3 className="font-bold mb-4">🔄 Обновление и Откат</h3>
        <div className="grid md:grid-cols-2 gap-4">
          <div className="bg-gray-800/30 rounded-lg p-4">
            <h4 className="text-sm font-bold mb-2 text-green-400">✅ Обновление</h4>
            <div className="space-y-2 text-xs text-gray-400">
              <div className="flex items-center gap-2"><span className="text-green-500">1.</span> Скачать новый билд</div>
              <div className="flex items-center gap-2"><span className="text-green-500">2.</span> Проверить SHA256 хеш</div>
              <div className="flex items-center gap-2"><span className="text-green-500">3.</span> Бэкап текущей версии</div>
              <div className="flex items-center gap-2"><span className="text-green-500">4.</span> Установить обновление</div>
              <div className="flex items-center gap-2"><span className="text-green-500">5.</span> Проверить работоспособность</div>
            </div>
          </div>
          <div className="bg-gray-800/30 rounded-lg p-4">
            <h4 className="text-sm font-bold mb-2 text-red-400">🔄 Откат</h4>
            <div className="space-y-2 text-xs text-gray-400">
              <div className="flex items-center gap-2"><span className="text-red-500">1.</span> Обнаружена ошибка</div>
              <div className="flex items-center gap-2"><span className="text-red-500">2.</span> Остановить сервис</div>
              <div className="flex items-center gap-2"><span className="text-red-500">3.</span> Восстановить бэкап</div>
              <div className="flex items-center gap-2"><span className="text-red-500">4.</span> Проверить целостность</div>
              <div className="flex items-center gap-2"><span className="text-red-500">5.</span> Запустить старую версию</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

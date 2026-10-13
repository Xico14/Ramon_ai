export default function InstallationView() {
  return (
    <div className="space-y-6">
      {/* Title */}
      <div>
        <h2 className="text-2xl font-bold mb-2">📦 Установка и Упаковка (Фаза 8)</h2>
        <p className="text-gray-400 text-sm">
          Финальный этап: превращаем Python-проект в обычную программу для Windows.
        </p>
      </div>

      {/* Build Pipeline */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
        <h3 className="font-bold mb-4">🔨 Процесс сборки</h3>
        <div className="flex flex-wrap items-center gap-2 justify-center">
          {[
            { label: 'Python код', icon: '🐍', sub: 'Исходники' },
            { label: 'Nuitka', icon: '⚙️', sub: 'Компиляция' },
            { label: 'C++ binary', icon: '💻', sub: 'Машинный код' },
            { label: 'Strip models', icon: '✂️', sub: 'Оптимизация' },
            { label: 'Package', icon: '📦', sub: 'Упаковка' },
            { label: 'Installer', icon: '🖥️', sub: 'Setup.exe' },
          ].map((step, i) => (
            <div key={i} className="flex items-center gap-2">
              <div className="bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-center min-w-[90px]">
                <div className="text-xl">{step.icon}</div>
                <div className="text-[10px] font-bold">{step.label}</div>
                <div className="text-[8px] text-gray-500">{step.sub}</div>
              </div>
              {i < 5 && <span className="text-gray-600">→</span>}
            </div>
          ))}
        </div>
      </div>

      {/* Nuitka Details */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
        <h3 className="font-bold mb-4">⚙️ Nuitka компиляция</h3>
        <div className="grid md:grid-cols-2 gap-4">
          <div>
            <h4 className="text-sm font-medium text-gray-400 mb-2">Преимущества</h4>
            <div className="space-y-2">
              {[
                'Код защищён (нельзя декомпилировать)',
                'Быстрее на 20-30%',
                'Не нужен Python на целевой машине',
                'Один exe-файл',
              ].map((item, i) => (
                <div key={i} className="flex items-center gap-2 text-xs text-gray-300">
                  <span className="text-green-400">✓</span>
                  {item}
                </div>
              ))}
            </div>
          </div>
          <div>
            <h4 className="text-sm font-medium text-gray-400 mb-2">Команда сборки</h4>
            <div className="bg-black/40 rounded-lg p-3 font-mono text-xs text-green-300 overflow-x-auto">
              <div>nuitka --standalone \</div>
              <div>  --onefile \</div>
              <div>  --enable-plugin=pyqt6 \</div>
              <div>  --include-data-dir=./models=models \</div>
              <div>  --windows-icon-from-ico=icon.ico \</div>
              <div>  --company-name="Jarvis AI" \</div>
              <div>  --product-name="Jarvis" \</div>
              <div>  main.py</div>
            </div>
          </div>
        </div>
      </div>

      {/* Model Stripping */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
        <h3 className="font-bold mb-4">✂️ Оптимизация моделей (Strip)</h3>
        <div className="grid md:grid-cols-3 gap-4">
          {[
            {
              model: 'Qwen2.5-3B',
              before: '6.5 GB (FP16)',
              after: '2.0 GB (Q4_K_M)',
              reduction: '69%',
              icon: '🧠',
            },
            {
              model: 'Whisper large-v3',
              before: '3.0 GB',
              after: '1.5 GB (int8)',
              reduction: '50%',
              icon: '🎤',
            },
            {
              model: 'TTS модель',
              before: '1.0 GB',
              after: '0.5 GB',
              reduction: '50%',
              icon: '🔊',
            },
          ].map((item) => (
            <div key={item.model} className="bg-gray-800/30 border border-gray-700 rounded-lg p-4">
              <div className="text-2xl mb-2">{item.icon}</div>
              <h4 className="font-bold text-sm mb-2">{item.model}</h4>
              <div className="space-y-1 text-xs">
                <div className="flex justify-between">
                  <span className="text-gray-500">До:</span>
                  <span className="text-red-400">{item.before}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">После:</span>
                  <span className="text-green-400">{item.after}</span>
                </div>
                <div className="flex justify-between border-t border-gray-700 pt-1 mt-1">
                  <span className="text-gray-500">Сжатие:</span>
                  <span className="text-blue-400 font-bold">{item.reduction}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Installer */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
        <h3 className="font-bold mb-4">🖥️ Установщик (Setup.exe)</h3>
        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <h4 className="text-sm font-medium text-gray-400 mb-3">Требования к системе</h4>
            <div className="space-y-2">
              {[
                { label: 'ОС', value: 'Windows 10/11 (64-bit)' },
                { label: 'RAM', value: 'Минимум 8 GB (рекомендуется 16 GB)' },
                { label: 'Диск', value: 'Минимум 10 GB свободного места' },
                { label: 'GPU', value: 'Опционально: NVIDIA с CUDA (ускорение)' },
                { label: 'CPU', value: '4+ ядра, AVX2 поддержка' },
                { label: 'Интернет', value: 'Не требуется (всё локально)' },
              ].map((req) => (
                <div key={req.label} className="flex items-center gap-2 text-xs">
                  <span className="text-gray-500 w-20">{req.label}:</span>
                  <span className="text-gray-300">{req.value}</span>
                </div>
              ))}
            </div>
          </div>
          <div>
            <h4 className="text-sm font-medium text-gray-400 mb-3">Что устанавливается</h4>
            <div className="space-y-2">
              {[
                { label: 'jarvis.exe', size: '~150 MB', desc: 'Основной исполняемый файл' },
                { label: 'models/', size: '~4 GB', desc: 'Нейросетевые модели' },
                { label: 'config/', size: '~1 MB', desc: 'Настройки (зашифрованы)' },
                { label: 'data/', size: '~0 MB', desc: 'Пустая папка для данных' },
              ].map((item) => (
                <div key={item.label} className="flex items-center gap-2 text-xs">
                  <span className="text-blue-400 font-mono w-24">{item.label}</span>
                  <span className="text-gray-500 w-16">{item.size}</span>
                  <span className="text-gray-400">{item.desc}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Installation Steps */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
        <h3 className="font-bold mb-4">📋 Процесс установки</h3>
        <div className="space-y-3">
          {[
            {
              step: 1,
              title: 'Запуск Setup.exe',
              desc: 'Пользователь запускает установщик от имени администратора',
              icon: '🚀',
            },
            {
              step: 2,
              title: 'Выбор папки установки',
              desc: 'По умолчанию: C:\\Program Files\\Jarvis AI\\',
              icon: '📁',
            },
            {
              step: 3,
              title: 'Копирование файлов',
              desc: 'Распаковка моделей и бинарников (~4.5 GB)',
              icon: '📦',
            },
            {
              step: 4,
              title: 'Создание ярлыков',
              desc: 'Ярлык на рабочем столе и в меню Пуск',
              icon: '🔗',
            },
            {
              step: 5,
              title: 'Первый запуск',
              desc: 'Проверка целостности, инициализация моделей',
              icon: '✅',
            },
            {
              step: 6,
              title: 'Готово!',
              desc: 'Джарвис готов к работе. Скажите "Джарвис" для активации',
              icon: '🤖',
            },
          ].map((item) => (
            <div key={item.step} className="flex items-start gap-3 p-3 bg-gray-800/30 rounded-lg">
              <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center text-sm font-bold flex-shrink-0">
                {item.step}
              </div>
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-lg">{item.icon}</span>
                  <h4 className="font-bold text-sm">{item.title}</h4>
                </div>
                <p className="text-xs text-gray-400">{item.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Clean VM Test */}
      <div className="bg-gradient-to-br from-gray-900 to-green-950 border border-gray-800 rounded-xl p-5">
        <h3 className="font-bold mb-4">🧪 Тест на чистой VM</h3>
        <p className="text-xs text-gray-400 mb-4">
          Финальная проверка: установка на виртуальную машину с чистой Windows 10/11
        </p>
        <div className="grid md:grid-cols-2 gap-4">
          <div>
            <h4 className="text-sm font-medium text-green-400 mb-2">Чеклист проверки</h4>
            <div className="space-y-2">
              {[
                'Установка проходит без ошибок',
                'Первый запуск успешен',
                'Wake Word работает',
                'STT распознаёт речь',
                'TTS генерирует звук',
                'LLM отвечает на вопросы',
                'Все инструменты работают',
                'Нет утечек памяти (1 час)',
              ].map((item, i) => (
                <div key={i} className="flex items-center gap-2 text-xs">
                  <span className="text-gray-600">⬜</span>
                  <span className="text-gray-300">{item}</span>
                </div>
              ))}
            </div>
          </div>
          <div>
            <h4 className="text-sm font-medium text-green-400 mb-2">Критерии успеха</h4>
            <div className="space-y-2 text-xs">
              <div className="bg-black/30 rounded p-2">
                <div className="font-bold text-green-400">✓ Установка &lt; 5 минут</div>
                <div className="text-gray-500">От запуска до первого ответа</div>
              </div>
              <div className="bg-black/30 rounded p-2">
                <div className="font-bold text-green-400">✓ 0 ошибок в логах</div>
                <div className="text-gray-500">Чистый первый запуск</div>
              </div>
              <div className="bg-black/30 rounded p-2">
                <div className="font-bold text-green-400">✓ Все функции работают</div>
                <div className="text-gray-500">Без дополнительных настроек</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Final Stats */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
        <h3 className="font-bold mb-4">📊 Финальные характеристики</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-black/30 rounded-lg p-3 text-center">
            <div className="text-2xl font-bold text-blue-400">~8 GB</div>
            <div className="text-xs text-gray-500">Размер дистрибутива</div>
          </div>
          <div className="bg-black/30 rounded-lg p-3 text-center">
            <div className="text-2xl font-bold text-green-400">&lt; 30 сек</div>
            <div className="text-xs text-gray-500">Холодный старт</div>
          </div>
          <div className="bg-black/30 rounded-lg p-3 text-center">
            <div className="text-2xl font-bold text-purple-400">~11 GB</div>
            <div className="text-xs text-gray-500">RAM в работе</div>
          </div>
          <div className="bg-black/30 rounded-lg p-3 text-center">
            <div className="text-2xl font-bold text-orange-400">1 файл</div>
            <div className="text-xs text-gray-500">Setup.exe</div>
          </div>
        </div>
      </div>
    </div>
  );
}

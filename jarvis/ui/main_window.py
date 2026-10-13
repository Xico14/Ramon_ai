"""
Main Window — Главное окно UI
PyQt6 + qasync для асинхронности
"""
import logging
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit, QStatusBar
)
from PyQt6.QtCore import Qt, QTimer

from core.event_bus import EventBus, Event, EventType
from core.fsm import FSM, State

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """Главное окно Джарвиса"""
    
    def __init__(self, event_bus: EventBus, fsm: FSM):
        super().__init__()
        
        self.event_bus = event_bus
        self.fsm = fsm
        
        self.setWindowTitle("🤖 Джарвис — AI Ассистент")
        self.setMinimumSize(600, 400)
        
        # Инициализация UI
        self._setup_ui()
        
        # Подписка на события
        self.event_bus.subscribe(EventType.STATE_CHANGED, self._on_state_changed)
        self.event_bus.subscribe(EventType.TEXT_TRANSCRIBED, self._on_user_text)
        self.event_bus.subscribe(EventType.LLM_RESPONSE_COMPLETED, self._on_assistant_text)
        
        # Статус бар
        self._update_status()
        
        logger.info("✅ UI создан")
    
    def _setup_ui(self) -> None:
        """Настройка интерфейса"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Заголовок
        title = QLabel("🤖 Джарвис")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; padding: 10px;")
        layout.addWidget(title)
        
        # Статус
        self.status_label = QLabel("Состояние: IDLE (Спит)")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("font-size: 14px; color: #888; padding: 5px;")
        layout.addWidget(self.status_label)
        
        # История диалога
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("""
            QTextEdit {
                background-color: #1a1a2e;
                color: #eee;
                border: 1px solid #333;
                border-radius: 8px;
                padding: 10px;
                font-size: 13px;
            }
        """)
        layout.addWidget(self.chat_display)
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        
        self.btn_speak = QPushButton("🎤 Говорить")
        self.btn_speak.clicked.connect(self._on_speak_clicked)
        self.btn_speak.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        buttons_layout.addWidget(self.btn_speak)
        
        self.btn_clear = QPushButton("🗑️ Очистить")
        self.btn_clear.clicked.connect(self._on_clear_clicked)
        self.btn_clear.setStyleSheet("""
            QPushButton {
                background-color: #555;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #666;
            }
        """)
        buttons_layout.addWidget(self.btn_clear)
        
        layout.addLayout(buttons_layout)
        
        # Status bar
        self.statusBar().showMessage("Готов к работе")
    
    def _on_state_changed(self, event: Event) -> None:
        """Обработка изменения состояния"""
        new_state = event.data.get('new_state', 'IDLE')
        
        state_labels = {
            'IDLE': '💤 Спит',
            'WAKE': '👂 Услышал',
            'LISTEN': '🎧 Слушает',
            'THINK': '💭 Думает',
            'SPEAK': '🗣️ Говорит',
            'BARGE_IN': '🛑 Перебит',
        }
        
        label = state_labels.get(new_state, new_state)
        self.status_label.setText(f"Состояние: {label}")
        
        # Обновление status bar
        self.statusBar().showMessage(f"FSM: {new_state}")
    
    def _on_user_text(self, event: Event) -> None:
        """Отображение текста пользователя"""
        text = event.data.get('text', '')
        self.chat_display.append(f"<b style='color: #64B5F6;'>Вы:</b> {text}")
    
    def _on_assistant_text(self, event: Event) -> None:
        """Отображение ответа ассистента"""
        text = event.data.get('response', '')
        self.chat_display.append(f"<b style='color: #81C784;'>Джарвис:</b> {text}")
    
    def _on_speak_clicked(self) -> None:
        """Кнопка 'Говорить' (PTT)"""
        # Имитация wake word
        import asyncio
        asyncio.create_task(self.event_bus.publish(Event(
            type=EventType.WAKE_DETECTED,
            data={'word': 'manual'},
            source='ui',
        )))
    
    def _on_clear_clicked(self) -> None:
        """Кнопка 'Очистить'"""
        self.chat_display.clear()
    
    def _update_status(self) -> None:
        """Обновление статуса"""
        stats = self.event_bus.stats
        self.statusBar().showMessage(
            f"Событий: {stats['published']} | "
            f"Доставлено: {stats['delivered']} | "
            f"Ошибок: {stats['failed']}"
        )
        
        # Обновление каждые 5 секунд
        QTimer.singleShot(5000, self._update_status)

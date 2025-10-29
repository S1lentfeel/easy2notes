import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QTextEdit, QPushButton, QLabel, QSplitter, QListWidgetItem
from PyQt6.QtCore import Qt

STYLESHEET = """
QMainWindow {
    background-color: #2c3e50;
}

QLabel {
    color: #ecf0f1;
    font-size: 14pt;
    font-weight: bold;
    margin-bottom: 5px;
}

QListWidget {
    background-color: #34495e;
    border: none;
    color: #ecf0f1;
    font-size: 11pt;
    outline: 0;
}

QListWidget::item:selected {
    background-color: #3498db;
    color: #ffffff;
}

QTextEdit {
    background-color: #34495e;
    border: none;
    color: #ecf0f1;
    font-size: 12pt;
    padding: 10px;
}

QPushButton {
    background-color: #3498db;
    color: #ffffff;
    border: none;
    padding: 10px 15px;
    font-size: 10pt;
    font-weight: bold;
    border-radius: 5px;
}

QPushButton:hover {
    background-color: #4aa3df;
}

QPushButton:pressed {
    background-color: #2980b9;
}

QSplitter::handle {
    background-color: #2c3e50;
}
QSplitter::handle:horizontal {
    width: 5px;
}

"""

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Easy2notes")
        self.setGeometry(200, 200, 1000, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        notes_label = QLabel("Мои заметки")
        self.notes_list_widget = QListWidget()
        left_layout.addWidget(notes_label)
        left_layout.addWidget(self.notes_list_widget)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        self.text_editor = QTextEdit()
        buttons_layout = QHBoxLayout()
        self.save_button = QPushButton("Сохранить")
        self.new_note_button = QPushButton("Новая заметка")
        self.logout_button = QPushButton("Выйти")
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.new_note_button)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.logout_button)
        right_layout.addWidget(self.text_editor)
        right_layout.addLayout(buttons_layout)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([300, 700])
        main_layout.addWidget(splitter)
        self.setStyleSheet(STYLESHEET)
        self.populate_placeholder_data()
        self.notes_list_widget.currentItemChanged.connect(self.note_selected)
        self.save_button.clicked.connect(self.save_note)
        self.new_note_button.clicked.connect(self.create_new_note)
        self.logout_button.clicked.connect(self.logout)

    def populate_placeholder_data(self):
        placeholder_notes = [
            "Список покупок.txt",
            "Идеи для проекта Яндекс.Лицея.txt",
            "Важные ссылки.md",
            "Рецепт борща.txt",
            "План на выходные.txt"
        ]
        self.notes_list_widget.addItems(placeholder_notes)
        self.notes_list_widget.setCurrentRow(0)
        self.text_editor.setPlaceholderText("Выберите заметку из списка, чтобы начать редактирование...")

    def note_selected(self, current_item: QListWidgetItem):
        if current_item is not None:
            note_title = current_item.text()
            self.text_editor.setText(
                f"1"
            )
        else:
            self.text_editor.clear()
            self.text_editor.setPlaceholderText("Выберите заметку из списка...")

    def save_note(self):
        current_item = self.notes_list_widget.currentItem()
        if current_item:
            note_title = current_item.text()
            note_content = self.text_editor.toPlainText()
        else:
            pass

    def create_new_note(self):
        new_note_name = f"Новая заметка {self.notes_list_widget.count() + 1}.txt"
        self.notes_list_widget.addItem(new_note_name)
        self.notes_list_widget.setCurrentRow(self.notes_list_widget.count() - 1)
        self.text_editor.clear()
        self.text_editor.setFocus()

    def logout(self):
        from login_and_register_gui import LoginMenu

        self.login_window = LoginMenu()
        self.login_window.show() 
        self.close()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
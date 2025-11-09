import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QTextEdit, QPushButton, QLabel, QSplitter, QListWidgetItem
from PyQt6.QtCore import Qt
from logic import get_folders_for_user, get_file_content, update_file_content, capture_face_encoding
from database import user_get_folder, get_face_encodings, store_face_encoding
from pathlib import Path
from PyQt6.QtWidgets import QMessageBox

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
    def __init__(self, username):
        super().__init__()
        self.active_user = username

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

        if not get_face_encodings(self.active_user):
            self.register_face_button = QPushButton("Зарегистрировать лицо")
            buttons_layout.addWidget(self.register_face_button)
            self.register_face_button.clicked.connect(self.register_face)

    def populate_placeholder_data(self):
        from login_and_register_gui import LoginMenu

        login_menu = LoginMenu()
        placeholder_notes = get_folders_for_user(self.active_user)
        self.notes_list_widget.addItems(placeholder_notes)
        self.notes_list_widget.setCurrentRow(0)
        self.text_editor.setPlaceholderText("Выберите заметку из списка, чтобы начать редактирование...")

    def note_selected(self, current_item: QListWidgetItem):
        if current_item is not None:
            note_filename = current_item.text()
            user_notes_folder = user_get_folder(self.active_user)
            full_path_to_note = Path(user_notes_folder) / note_filename
            content = get_file_content(full_path_to_note)
            self.text_editor.setText(content)
        else:
            self.text_editor.clear()
            self.text_editor.setPlaceholderText("Выберите заметку из списка...")

    def save_note(self):
        current_item = self.notes_list_widget.currentItem()
        if current_item:
            note_filename = current_item.text()
            note_content = self.text_editor.toPlainText()
            user_notes_folder = user_get_folder(self.active_user)
            full_path_to_note = Path(user_notes_folder) / note_filename
            update_file_content(full_path_to_note, note_content)
        else:
            pass

    def create_new_note(self):
        new_note_name = f"{self.notes_list_widget.count() + 1}.txt"
        user_notes_folder = user_get_folder(self.active_user)
        full_path_to_note = Path(user_notes_folder) / new_note_name

        try:
            with open(full_path_to_note, 'w', encoding='utf-8') as f:
                pass
            self.notes_list_widget.addItem(new_note_name)
            self.notes_list_widget.setCurrentRow(self.notes_list_widget.count() - 1)
            self.text_editor.clear()
            self.text_editor.setFocus()
        except Exception:
            pass

    def register_face(self):
        try:
            encoding = capture_face_encoding()
            store_face_encoding(self.active_user, encoding.tolist())
            QMessageBox.information(self, "Успех", "Лицо зарегистрировано!")
            self.register_face_button.hide()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось зарегистрировать лицо: {str(e)}")

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
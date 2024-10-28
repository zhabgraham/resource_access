from PyQt6 import QtWidgets, QtGui
from PyQt6.QtWidgets import QApplication, QFileDialog, QMessageBox, QMainWindow, QLabel, QLineEdit, QPushButton, QTextEdit
import os
import sys

class ResourceAccessApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Система доступу до файлів")
        self.setGeometry(100, 100, 800, 600)

        self.label = QLabel("Введіть ім'я користувача:", self)
        self.label.setGeometry(20, 20, 200, 30)

        self.user_entry = QLineEdit(self)
        self.user_entry.setGeometry(220, 20, 200, 30)

        self.select_dir_button = QPushButton("Вибрати директорію", self)
        self.select_dir_button.setGeometry(20, 70, 200, 30)
        self.select_dir_button.clicked.connect(self.select_directory)

        self.get_access_button = QPushButton("Отримати доступні файли", self)
        self.get_access_button.setGeometry(240, 70, 200, 30)
        self.get_access_button.clicked.connect(self.get_user_resources)

        self.get_readable_for_all_button = QPushButton("Файли, доступні для читання всім користувачам", self)
        self.get_readable_for_all_button.setGeometry(460, 70, 300, 30)
        self.get_readable_for_all_button.clicked.connect(self.get_readable_for_all_resources)

        self.result_text = QTextEdit(self)
        self.result_text.setGeometry(20, 120, 760, 450)
        self.result_text.setReadOnly(True)

        self.selected_directory = None

    def select_directory(self):
        self.selected_directory = QFileDialog.getExistingDirectory(self, "Вибрати директорію")
        if self.selected_directory:
            QMessageBox.information(self, "Вибрана директорія", f"Вибрана директорія: {self.selected_directory}")

    def get_user_resources(self):
        user = self.user_entry.text()
        if user and self.selected_directory:
            read_resources = []
            write_resources = []
            if os.path.exists(self.selected_directory):
                for root_dir, dirs, files in os.walk(self.selected_directory):
                    for file in files:
                        file_path = os.path.join(root_dir, file)
                        if os.access(file_path, os.R_OK):
                            read_resources.append(file_path)
                        if os.access(file_path, os.W_OK):
                            write_resources.append(file_path)
                read_resources_str = "\n".join(read_resources)
                write_resources_str = "\n".join(write_resources)
                message = f"Файли для читання:\n{read_resources_str}\n\nФайли для запису:\n{write_resources_str}"
            else:
                message = "Вибрана директорія не існує."
        elif not user:
            message = "Введіть ім'я користувача."
        else:
            message = "Будь ласка, виберіть директорію."
        self.result_text.setPlainText(message)

    def get_readable_for_all_resources(self):
        readable_for_all = []
        if self.selected_directory:
            for root_dir, dirs, files in os.walk(self.selected_directory):
                for file in files:
                    file_path = os.path.join(root_dir, file)
                    if os.access(file_path, os.R_OK):
                        stat_info = os.stat(file_path)
                        if stat_info.st_mode & 0o004: 
                            readable_for_all.append(file_path)
            message = "\n".join(readable_for_all) if readable_for_all else "Немає файлів, доступних для читання всім користувачам."
        else:
            message = "Будь ласка, виберіть директорію."
        self.result_text.setPlainText(message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ResourceAccessApp()
    window.show()

    print("[Тест] Вибір директорії")
    window.selected_directory = "/home/sasha/Documents/blink/"
    if window.selected_directory:
        print("  -> Вибрана директорія: ", window.selected_directory)
    else:
        print("  -> Директорія не вибрана")

    print("[Тест] Отримання доступних файлів")
    window.user_entry.setText("nastia")
    window.get_user_resources()
    print("  -> Результат: \n", window.result_text.toPlainText())

    print("[Тест] Файли, доступні для читання всім користувачам")
    window.get_readable_for_all_resources()
    print("  -> Результат: \n", window.result_text.toPlainText())

    sys.exit(app.exec())


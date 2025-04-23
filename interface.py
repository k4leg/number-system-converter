import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox, QTextEdit, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QFont, QRegExpValidator
from PyQt5.QtCore import QRegExp, Qt
from converter import convert_base
import os

class BaseConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.history = []  # Инициализация истории в начале
        self.load_history()
        self.initUI()

    def initUI(self):
        # Настройка окна
        self.setWindowTitle('Конвертер систем счисления')
        self.setFixedSize(700, 500)  # Увеличенный размер окна

        # Основной шрифт для текста
        font = QFont("Arial", 12)

        layout = QVBoxLayout()

        # Выбор системы счисления ввода
        self.from_base_label = QLabel('Из системы счисления:')
        self.from_base_label.setFont(font)
        layout.addWidget(self.from_base_label)

        self.from_base_combobox = QComboBox(self)
        self.from_base_combobox.setFont(font)
        self.from_base_combobox.addItems([str(i) for i in range(2, 37)])
        self.from_base_combobox.currentIndexChanged.connect(self.update_input_validator)
        layout.addWidget(self.from_base_combobox)

        # Поле ввода числа
        self.number_input = QLineEdit(self)
        self.number_input.setFont(font)
        self.number_input.setPlaceholderText('Введите число')
        layout.addWidget(self.number_input)

        # Выбор системы счисления вывода
        self.to_base_label = QLabel('В систему счисления:')
        self.to_base_label.setFont(font)
        layout.addWidget(self.to_base_label)

        self.to_base_combobox = QComboBox(self)
        self.to_base_combobox.setFont(font)
        self.to_base_combobox.addItems([str(i) for i in range(2, 37)])
        layout.addWidget(self.to_base_combobox)

        # Кнопка конвертации
        self.convert_button = QPushButton('Конвертировать', self)
        self.convert_button.setFont(font)
        self.convert_button.clicked.connect(self.convert)
        layout.addWidget(self.convert_button)

        # Поле для результата
        self.result_label = QLabel('Результат: ', self)
        self.result_label.setFont(font)
        layout.addWidget(self.result_label)

        # Добавление пространства между ответом и историей
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer)

        # Поле для истории
        self.history_label = QLabel('История конвертаций:', self)
        self.history_label.setFont(font)
        layout.addWidget(self.history_label)

        self.history_text = QTextEdit(self)
        self.history_text.setFont(font)
        self.history_text.setReadOnly(True)
        layout.addWidget(self.history_text)

        self.setLayout(layout)
        self.update_input_validator()
        self.display_history()

    def update_input_validator(self):
        from_base = int(self.from_base_combobox.currentText())
        allowed_chars = self.base_to_chars(from_base)

        # Разрешаем знак минус и точку
        regex_pattern = f"^-?[{allowed_chars}]*(\\.[{allowed_chars}]*)?$"

        regex = QRegExp(regex_pattern)
        validator = QRegExpValidator(regex, self.number_input)
        self.number_input.setValidator(validator)

    def base_to_chars(self, base):
        if base < 10:
            return ''.join([str(i) for i in range(base)])
        else:
            return ''.join([str(i) for i in range(10)] + [chr(ord('A') + i) for i in range(base - 10)])

    def convert(self):
        number = self.number_input.text()
        from_base = int(self.from_base_combobox.currentText())
        to_base = int(self.to_base_combobox.currentText())
        try:
            result = convert_base(number, from_base, to_base)
            self.result_label.setText(f'Результат: <b>{result}</b>')  # Жирный текст для ответа
            self.history.append(f"Конвертация {number} из {from_base} в {to_base}: {result}")
            self.save_history()
            self.display_history()
        except ValueError as e:
            QMessageBox.critical(self, 'Ошибка', str(e))

    def display_history(self):
        self.history_text.setText("\n".join(self.history))

    def save_history(self):
        with open("conversion_history.txt", "w") as file:
            file.write("\n".join(self.history))

    def load_history(self):
        if os.path.exists("conversion_history.txt"):
            with open("conversion_history.txt", "r") as file:
                self.history = file.read().splitlines()

def create_interface():
    app = QApplication(sys.argv)
    ex = BaseConverterApp()
    ex.show()
    sys.exit(app.exec_())

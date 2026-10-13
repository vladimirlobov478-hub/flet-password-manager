from PyQt6.QtWidgets import (
    QPushButton,
    QLineEdit,
    QLabel,
    QListWidget,
    QGroupBox,
    QStatusBar,
    QCheckBox,
    QSpinBox,
    QProgressBar,
    QFrame
)


class MyButton(QPushButton):
    def __init__(self, text=""):
        super().__init__(text)
        self.setMinimumHeight(30)


class MyLineEdit(QLineEdit):
    def __init__(self, placeholder=""):
        super().__init__()
        self.setPlaceholderText(placeholder)


class MyLabel(QLabel):
    def __init__(self, text=""):
        super().__init__(text)


class MyListWidget(QListWidget):
    def __init__(self):
        super().__init__()


class MyGroupBox(QGroupBox):
    def __init__(self, title=""):
        super().__init__(title)


class MyStatusBar(QStatusBar):
    def __init__(self):
        super().__init__()


class MyCheckBox(QCheckBox):
    def __init__(self, text=""):
        super().__init__(text)


class MySpinBox(QSpinBox):
    def __init__(self):
        super().__init__()
        self.setMinimum(4)
        self.setMaximum(50)
        self.setValue(8)


class MyProgressBar(QProgressBar):
    def __init__(self):
        super().__init__()
        self.setValue(0)


class MyFrame(QFrame):
    def __init__(self):
        super().__init__()
class SimpleStorage:
    
    def __init__(self):
        self.data_list = []

    def add_or_update(self, key, value):
        found = False
        for i in range(len(self.data_list)):
            pair = self.data_list[i]
            if pair[0] == key:
                self.data_list[i] = (key, value)
                found = True
                break
        if found == False:
            self.data_list.append((key, value))

    def get_value(self, key):
        for pair in self.data_list:
            if pair[0] == key:
                return pair[1]
        return None
from abc import ABC, abstractmethod


class AbstractEntity(ABC):
    @abstractmethod
    def display_name(self):
        pass

    @abstractmethod
    def validate(self):
        pass


class PasswordEntry(AbstractEntity):
    def __init__(self, service, login, password, category="Общее"):
        self._service = ""
        self._login = ""
        self._password = ""
        self._category = ""

        self.service = service
        self.login = login
        self.password = password
        self.category = category

    @property
    def service(self):
        return self._service

    @service.setter
    def service(self, value):
        text = str(value).strip()
        if text == "":
            raise ValueError("Название сервиса не может быть пустым!")
        self._service = text

    @property
    def login(self):
        return self._login

    @login.setter
    def login(self, value):
        text = str(value).strip()
        if text == "":
            raise ValueError("Логин не может быть пустым!")
        self._login = text

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        text = str(value)
        if text == "":
            raise ValueError("Пароль не может быть пустым!")
        self._password = text

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        text = str(value).strip()
        if text == "":
            self._category = "Общее"
        else:
            self._category = text

    def display_name(self):
        return self._service + " (" + self._login + ")"

    def validate(self):
        if len(self._service) > 0 and len(self._login) > 0 and len(self._password) > 0:
            return True
        return False

    def __repr__(self):
        return f"PasswordEntry('{self._service}', '{self._login}')"

    def __str__(self):
        return f"[{self._category}] {self._service} -> {self._login}"

    def __eq__(self, other):
        if not isinstance(other, PasswordEntry):
            return False
        service_same = self._service.lower() == other._service.lower()
        login_same = self._login.lower() == other._login.lower()
        return service_same and login_same

    def __lt__(self, other):
        return self._service.lower() < other._service.lower()

    def __len__(self):
        return len(self._password)

    def __hash__(self):
        return hash((self._service.lower(), self._login.lower()))


class AppUser(AbstractEntity):
    def __init__(self, username):
        self._username = ""
        self.username = username

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, val):
        cleaned = str(val).strip()
        if cleaned == "":
            self._username = "Admin"
        else:
            self._username = cleaned

    def display_name(self):
        return self._username

    def validate(self):
        return len(self._username) > 0

    def __repr__(self):
        return f"AppUser('{self._username}')"

    def __str__(self):
        return self._username
class PasswordHelper:
    @staticmethod
    def calculate_strength(pwd):
        
        score = 0
        if len(pwd) >= 8:
            score += 30

        has_upper = False
        has_lower = False
        has_digit = False
        has_special = False

        for char in pwd:
            if char.isupper():
                has_upper = True
            elif char.islower():
                has_lower = True
            elif char.isdigit():
                has_digit = True
            else:
                has_special = True

        if has_upper:
            score += 20
        if has_lower:
            score += 20
        if has_digit:
            score += 15
        if has_special:
            score += 15

        if score > 100:
            score = 100
        return score

    @staticmethod
    def write_report_file(file_path, user_name, start_time, end_time):
        """Запись ASCII-отчета в файл."""
        fmt = "%d.%m.%Y %H:%M:%S"
        t_start = start_time.strftime(fmt)
        t_end = end_time.strftime(fmt)

        border = "+----------+---------------------+---------------------+\n"
        header = "| login    | time_in             | time_out            |\n"
        row    = f"| {user_name:<8} | {t_start} | {t_end} |\n"

        file = open(file_path, "w", encoding="utf-8")
        file.write(border)
        file.write(header)
        file.write(border)
        file.write(row)
        file.write(border)
        file.close()
import sys
from datetime import datetime

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLineEdit,
    QMessageBox
)

from storage import SimpleStorage
from models import PasswordEntry, AppUser
from widgets import (
    MyButton,
    MyLineEdit,
    MyLabel,
    MyListWidget,
    MyGroupBox,
    MyStatusBar,
    MyCheckBox,
    MySpinBox,
    MyProgressBar,
    MyFrame
)
from helpers import PasswordHelper


class MainWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.time_opened = datetime.now()

        self.entries = []
        self.seed_data()

        self.cache = SimpleStorage()
        self.sync_cache()

        self.setup_ui()
        self.update_list_display()

    def seed_data(self):
        self.entries.append(PasswordEntry("VK", "id12345", "Pass123!", "Соцсети"))
        self.entries.append(PasswordEntry("Telegram", "+79990001122", "TgPass2026!", "Мессенджеры"))
        self.entries.append(PasswordEntry("GitHub", "my_nickname", "Git_Token_99", "Работа"))
        self.entries.append(PasswordEntry("Mail.ru", "box@mail.ru", "SecretMail!1", "Почта"))
        self.entries.append(PasswordEntry("Yandex", "coder_ya", "YandexK3y#", "Почта"))
        self.entries.append(PasswordEntry("Steam", "gamer_boy", "SteamGa-me77", "Игры"))
        self.entries.append(PasswordEntry("Gosuslugi", "123-456-789 00", "G0s_Usligi2026", "Госуслуги"))
        self.entries.append(PasswordEntry("SberBank", "client_99", "Sb3r#SafeP@ss", "Банки"))
        self.entries.append(PasswordEntry("Tinkoff", "card_holder", "T1nk0ff$Cash", "Банки"))
        self.entries.append(PasswordEntry("Discord", "chat_user", "D!sc0rdP@ss", "Общение"))
        self.entries.append(PasswordEntry("WorkVPN", "employee_1", "VpnAccess#99", "Работа"))

    def sync_cache(self):
        for item in self.entries:
            key = item.service + ":" + item.login
            self.cache.add_or_update(key, item)

    def setup_ui(self):
        self.setWindowTitle("Менеджер паролей")
        self.resize(800, 500)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)

        # Левая колонка
        left_group = MyGroupBox("Список записей")
        left_layout = QVBoxLayout()
        left_group.setLayout(left_layout)

        self.list_widget = MyListWidget()
        self.list_widget.currentRowChanged.connect(self.select_entry)
        left_layout.addWidget(self.list_widget)

        self.btn_sort = MyButton("Сортировать по названию")
        self.btn_sort.clicked.connect(self.sort_items)
        left_layout.addWidget(self.btn_sort)

        self.btn_del = MyButton("Удалить выбранное")
        self.btn_del.clicked.connect(self.delete_item)
        left_layout.addWidget(self.btn_del)

        main_layout.addWidget(left_group)

        # Правая колонка
        right_group = MyGroupBox("Форма редактирования")
        form_layout = QGridLayout()
        right_group.setLayout(form_layout)

        form_layout.addWidget(MyLabel("Сервис:"), 0, 0)
        self.txt_service = MyLineEdit("Пример: Google")
        form_layout.addWidget(self.txt_service, 0, 1)

        form_layout.addWidget(MyLabel("Логин:"), 1, 0)
        self.txt_login = MyLineEdit("Логин / Почта")
        form_layout.addWidget(self.txt_login, 1, 1)

        form_layout.addWidget(MyLabel("Категория:"), 2, 0)
        self.txt_category = MyLineEdit("Например: Учёба")
        form_layout.addWidget(self.txt_category, 2, 1)

        form_layout.addWidget(MyLabel("Пароль:"), 3, 0)
        self.txt_password = MyLineEdit("Введите пароль")
        self.txt_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.txt_password.textChanged.connect(self.check_pwd_strength)
        form_layout.addWidget(self.txt_password, 3, 1)

        self.chk_show = MyCheckBox("Показать пароль")
        self.chk_show.toggled.connect(self.toggle_show_pwd)
        form_layout.addWidget(self.chk_show, 4, 1)

        form_layout.addWidget(MyLabel("Надёжность:"), 5, 0)
        self.pbar = MyProgressBar()
        form_layout.addWidget(self.pbar, 5, 1)

        opt_frame = MyFrame()
        frame_layout = QHBoxLayout()
        opt_frame.setLayout(frame_layout)
        frame_layout.addWidget(MyLabel("Мин. символов в пароле:"))
        self.spin_len = MySpinBox()
        frame_layout.addWidget(self.spin_len)
        form_layout.addWidget(opt_frame, 6, 0, 1, 2)

        self.btn_save = MyButton("Сохранить запись")
        self.btn_save.clicked.connect(self.save_entry)
        form_layout.addWidget(self.btn_save, 7, 0, 1, 2)

        main_layout.addWidget(right_group)

        # Статусбар
        self.status = MyStatusBar()
        self.setStatusBar(self.status)

    def update_list_display(self):
        self.list_widget.clear()
        for item in self.entries:
            self.list_widget.addItem(str(item))
        total = len(self.entries)
        self.status.showMessage(f"Пользователь: {self.user.username} | Всего записей: {total}")

    def check_pwd_strength(self):
        pwd = self.txt_password.text()
        strength = PasswordHelper.calculate_strength(pwd)
        self.pbar.setValue(strength)

    def toggle_show_pwd(self):
        if self.chk_show.isChecked():
            self.txt_password.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.txt_password.setEchoMode(QLineEdit.EchoMode.Password)

    def select_entry(self, index):
        if index >= 0 and index < len(self.entries):
            chosen = self.entries[index]
            self.txt_service.setText(chosen.service)
            self.txt_login.setText(chosen.login)
            self.txt_category.setText(chosen.category)
            self.txt_password.setText(chosen.password)

    def save_entry(self):
        s = self.txt_service.text()
        l = self.txt_login.text()
        c = self.txt_category.text()
        p = self.txt_password.text()

        if len(p) < self.spin_len.value():
            QMessageBox.warning(self, "Ошибка", f"Пароль должен быть от {self.spin_len.value()} символов!")
            return

        try:
            item = PasswordEntry(s, l, p, c)
        except ValueError as err:
            QMessageBox.warning(self, "Ошибка валидации", str(err))
            return

        found_index = -1
        for i in range(len(self.entries)):
            if self.entries[i] == item:
                found_index = i
                break

        if found_index != -1:
            self.entries[found_index] = item
        else:
            self.entries.append(item)

        self.cache.add_or_update(item.service + ":" + item.login, item)
        self.update_list_display()

    def delete_item(self):
        row = self.list_widget.currentRow()
        if row >= 0 and row < len(self.entries):
            del self.entries[row]
            self.update_list_display()
        else:
            QMessageBox.information(self, "Инфо", "Сначала выберите строку в списке.")

    def sort_items(self):
        self.entries.sort()
        self.update_list_display()

    def closeEvent(self, event):
        time_closed = datetime.now()
        PasswordHelper.write_report_file("session_report.txt", self.user.username, self.time_opened, time_closed)
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    user = AppUser("UserName")
    window = MainWindow(user)
    window.show()
    sys.exit(app.exec())

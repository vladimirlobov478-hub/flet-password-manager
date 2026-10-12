import flet as ft
import json
import os

# Файл, где храним пароли
FILE_NAME = "passwords.json"


def load_passwords():
    # Если файла ещё нет - возвращаем пустой список
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        return json.load(f)


def save_passwords(data):
    # Сохраняем весь список в JSON
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main(page: ft.Page):
    page.title = "Мой менеджер паролей"
    page.window_width = 450
    page.window_height = 600

    passwords = load_passwords()

    # Поля ввода
    site_input = ft.TextField(label="Название сервиса (например, ВКонтакте)")
    login_input = ft.TextField(label="Логин или почта")
    password_input = ft.TextField(label="Пароль", password=True, can_reveal_password=True)

    # Список, куда будем выводить карточки
    cards_list = ft.ListView(expand=True, spacing=10)

    # Функция обновления списка на экране
    def update_view():
        cards_list.controls.clear()
        for item in passwords:
            cards_list.controls.append(
                ft.Card(
                    content=ft.Container(
                        padding=10,
                        content=ft.Column([
                            ft.Text(item["site"], size=16, weight=ft.FontWeight.BOLD),
                            ft.Text(f"Логин: {item['login']}"),
                            ft.Text(f"Пароль: {item['password']}"),
                        ])
                    )
                )
            )
        page.update()

    # Обработчик нажатия на кнопку "Сохранить"
    def add_clicked(e):
        site = site_input.value.strip()
        login = login_input.value.strip()
        pwd = password_input.value.strip()

        if not site or not pwd:
            return  # Не сохраняем, если сервис или пароль пустые

        # Добавляем новую запись
        passwords.append({
            "site": site,
            "login": login,
            "password": pwd
        })

        # Сохраняем в файл на диске
        save_passwords(passwords)

        # Очищаем поля ввода
        site_input.value = ""
        login_input.value = ""
        password_input.value = ""

        update_view()

    add_button = ft.ElevatedButton("Сохранить пароль", on_click=add_clicked)

    # Добавляем все элементы на окно
    page.add(
        site_input,
        login_input,
        password_input,
        add_button,
        ft.Divider(),
        cards_list
    )

    # Загружаем сохранённые пароли при старте
    update_view()


if __name__ == "__main__":
    ft.app(target=main)

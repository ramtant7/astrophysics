import requests
import json


def authorize_and_save_credentials(username, password):
    url = "https://example.com/login"  # Замените на реальный URL страницы входа
    login_data = {"username": username, "password": password}

    with requests.Session() as session:
        response = session.post(url, data=login_data)

        if response.status_code == 200:
            print("Успешная авторизация!")

            # Сохраняем логин и пароль в файловой базе данных
            save_credentials_to_file(password, username)
        else:
            print(f"Произошла ошибка при авторизации. Код статуса: {response.status_code}")


def save_credentials_to_file(password, login):
    credentials = {password: login}  # Форматируем данные для записи в файл

    try:
        with open('credentials.json', 'w') as file:
            json.dump(credentials, file, indent=4)
        print("Учетные данные успешно сохранены.")
    except Exception as e:
        print(f"Произошла ошибка при сохранении учетных данных: {e}")


# Пример использования функции
authorize_and_save_credentials("your_username", "your_password")
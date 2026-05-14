import httpx
import time

API_URL = "http://127.0.0.1:8000"

def run_tests():
    with httpx.Client() as client:
        print("Обновляем валюты...")
        r = client.post(f"{API_URL}/currencies/update")
        print(f"Статус обновления: {r.status_code}")
        assert r.status_code == 200

        print("Получаем валюты...")
        r = client.get(f"{API_URL}/currencies/")
        currencies = r.json()
        print(f"Найдено {len(currencies)} валют. Первая: {currencies[0]['code']}")
        assert len(currencies) > 0

        print("Создаем пользователя...")
        timestamp = int(time.time())
        r = client.post(f"{API_URL}/users/", json={"username": f"testuser_{timestamp}", "email": f"test_{timestamp}@example.com"})
        print(f"Статус создания пользователя: {r.status_code}, Ответ: {r.json()}")
        assert r.status_code == 201
        user_id = r.json()['id']

        print("Подписываемся на валюту...")
        currency_code = currencies[0]['code']
        r = client.post(f"{API_URL}/subscriptions/", json={"user_id": user_id, "currency_code": currency_code})
        print(f"Статус подписки: {r.status_code}, Ответ: {r.json()}")
        assert r.status_code == 201

        print("Получаем данные пользователя...")
        r = client.get(f"{API_URL}/users/{user_id}")
        user_details = r.json()
        print(f"Подписки пользователя: {user_details['subscribed_currencies']}")
        assert len(user_details['subscribed_currencies']) == 1
        assert user_details['subscribed_currencies'][0]['code'] == currency_code

        print("ВСЕ ТЕСТЫ ПРОЙДЕНЫ")

if __name__ == "__main__":
    run_tests()

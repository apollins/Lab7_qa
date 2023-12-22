import pytest
import parser

class TestSuite:

    # Перевірка підключення клієнта iperf3
    @pytest.mark.usefixtures("server")
    def test_iperf3_client_connection(self, client):
        try:
            # Перевірка успішності підключення клієнта
            if client.returncode == 0:
                # Якщо підключення успішне, розбираємо вивід та перевіряємо певні метрики
                for value in parser.parser(client):
                    print(value)
                    assert value["Transfer"] > 2 and value["Bandwidth"] > 20
            else:
                # Якщо підключення не вдалося, викидаємо виключення з повідомленням про помилку
                raise Exception(parser.parse_error(client))

        except Exception as e:
            print(f"Помилка під час перевірки підключення клієнта iperf3: {e}")
            raise

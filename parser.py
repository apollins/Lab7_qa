import json
import math


def parser(iperf_result):
    try:
        parsed_intervals = json.loads(iperf_result.stdout)["intervals"]
        return list(map(lambda interval: parse_interval(interval), parsed_intervals))
    except (json.JSONDecodeError, KeyError) as e:
        # Обробка помилок, якщо виникли під час розбору JSON або відсутність очікуваних ключів
        print(f"Помилка під час розбору результатів iperf: {e}")
        return []


def parse_interval(interval):
    try:
        interval_sum = interval["sum"]
        return {
            "Interval": f"{interval_sum['start']:.{1}f}-{interval_sum['end']:.{1}f}",
            "Transfer": float(f"{interval_sum['bytes'] / math.pow(10, 6):.{2}f}"),
            "Transfer_unit": "MBytes",
            "Bandwidth": float(f"{interval_sum['bits_per_second'] / math.pow(10, 6):.{2}f}"),
            "Bandwidth_unit": "Mbits/sec"
        }
    except (KeyError, ValueError) as e:
        # Обробка помилок, якщо виникли під час розбору конкретного інтервалу
        print(f"Помилка під час розбору інтервалу: {e}")
        return {
            "Interval": "N/A",
            "Transfer": 0.0,
            "Transfer_unit": "MBytes",
            "Bandwidth": 0.0,
            "Bandwidth_unit": "Mbits/sec"
        }


def parse_error(iperf_result):
    try:
        json_result = json.loads(iperf_result.stdout)
        return json_result["error"]
    except (json.JSONDecodeError, KeyError) as e:
        # Обробка помилок, якщо виникли під час розбору JSON або відсутність очікуваних ключів
        print(f"Помилка під час розбору результатів iperf: {e}")
        return "N/A"

from decimal import Decimal, getcontext
from collections import OrderedDict, defaultdict

getcontext().prec = 10


def get_unique_characters(message):
    seen = set()
    unique = []
    for char in message:
        if char not in seen:
            seen.add(char)
            unique.append(char)
    return unique


def calculate_frequencies(message, unique_chars):
    freq = defaultdict(int)
    for char in message:
        freq[char] += 1
    return {char: Decimal(count) for char, count in freq.items()}


def sort_by_frequency(freq_dict):
    return OrderedDict(sorted(freq_dict.items(), key=lambda item: item[1]))


def normalize_frequencies(sorted_freq, total):
    return {char: freq / Decimal(total) for char, freq in sorted_freq.items()}


def assign_intervals(probabilities):
    intervals = {}
    current = Decimal('0')
    for char, prob in probabilities.items():
        start = current
        end = start + prob
        intervals[char] = (start, end)
        current = end
    return intervals


def update_intervals(current_interval, probabilities):
    new_intervals = {}
    span = current_interval[1] - current_interval[0]
    current = current_interval[0]
    for char, prob in probabilities.items():
        start = current
        end = start + span * prob
        new_intervals[char] = (start, end)
        current = end
    return new_intervals


def print_intervals(intervals):
    for char, (start, end) in intervals.items():
        display_char = f"'{char}'" if char == ' ' else char
        print(f"{display_char}: [{start}; {end})")


def main():
    message = input("Введите сообщение: ")

    if not message:
        print("Ошибка: Входное сообщение пусто.")
        return

    unique_chars = get_unique_characters(message)
    frequencies = calculate_frequencies(message, unique_chars)
    sorted_freq = sort_by_frequency(frequencies)
    total_length = len(message)
    probabilities = normalize_frequencies(sorted_freq, total_length)

    sorted_alphabet = list(probabilities.keys())
    print(f"Отсортированный алфавит: {sorted_alphabet}\n")

    initial_intervals = assign_intervals(probabilities)
    print("Начальные интервалы:")
    print_intervals(initial_intervals)
    print()

    main_interval = (Decimal('0'), Decimal('1'))
    current_intervals = initial_intervals.copy()

    for idx, char in enumerate(message, 1):
        if char not in current_intervals:
            print(f"Ошибка: Символ '{char}' не найден в интервалах.")
            return

        main_interval = current_intervals[char]

        current_intervals = update_intervals(main_interval, probabilities)

        print(f"После обработки символа {idx} ('{char}'):")
        print_intervals(current_intervals)
        print("==========================")

    average = (main_interval[0] + main_interval[1]) / 2
    print(f"Среднее значение финального интервала: {average}")
    print(f"Финальный интервал: [{main_interval[0]}; {main_interval[1]})")


if __name__ == "__main__":
    main()

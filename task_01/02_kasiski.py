'''Реалізація тесту Касіскі для визначення довжини ключа у шифрі Віженера'''
from collections import defaultdict

def find_repeated_sequences(ciphertext, sequence_length=3):
    '''Знаходимо повторювані послідовності у шифротексті.'''
    sequences = defaultdict(list)
    for i in range(len(ciphertext) - sequence_length + 1):
        sequence = ciphertext[i:i + sequence_length]
        sequences[sequence].append(i)
    return {seq: pos for seq, pos in sequences.items() if len(pos) > 1}


def calculate_distances(positions):
    '''Розраховуємо відстані між позиціями.'''
    return [positions[i] - positions[i - 1] for i in range(1, len(positions))]


def find_common_divisors(distances):
    '''Знаходимо дільники відстаней.'''
    def get_all_divisors(n):
        divisors = set()
        for i in range(2, n//2 + 1):
            if n % i == 0:
                divisors.add(i)
        if n > 1:
            divisors.add(n)
        return divisors

    all_divisors = defaultdict(int)
    for distance in distances:
        for divisor in get_all_divisors(distance):
            all_divisors[divisor] += 1

    res = sorted(all_divisors.items(), key=lambda x: x[1], reverse=True)
    return res


def filter_divisors(divisors):
    '''Фільтруємо дільники для знаходження найбільш імовірної довжини ключа.'''
    # Сортуємо за спаданням частоти
    divisors = sorted(divisors, key=lambda x: x[1], reverse=True)

    # Беремо перших 10 дільників
    top_divisors = [d[0] for d in divisors[:10]]

    # Проходимося по факторам, починаючи з найбільшого
    for factor in sorted(top_divisors, reverse=True):
        # Витягуємо всі фактори, які мають більшу або рівну частоту
        relevant_divisors = [d for d in divisors if d[1]
                             >= divisors[top_divisors.index(factor)][1]]

        # Перевіряємо, чи ділиться поточний фактор на ці фактори
        if all(factor % d[0] == 0 for d in relevant_divisors):
            # Обчислюємо середню частоту цих факторів
            avg_frequency = sum(
                d[1] for d in relevant_divisors) / len(relevant_divisors)

            # Якщо частота фактора значно нижча за середнє, відкидаємо його
            factor_frequency = divisors[top_divisors.index(factor)][1]
            if factor_frequency < 0.75 * avg_frequency:  # Поріг 75%, можна налаштувати
                continue

            return factor
        # return top_divisors[0]


def kasiski_analysis(ciphertext, sequence_length=3):
    '''Реалізація аналізу Касіскі.'''
    repeated_sequences = find_repeated_sequences(ciphertext, sequence_length)
    distances = []
    for positions in repeated_sequences.values():
        distances.extend(calculate_distances(positions))

    if not distances:
        return "Не знайдено повторюваних послідовностей."

    common_divisors = find_common_divisors(distances)

    return filter_divisors(common_divisors), common_divisors


CIPHERTEXT_FILE = 'task_01/cipher_text.txt'
with open(CIPHERTEXT_FILE, 'r', encoding='utf-8') as file:
    cipher_text = file.read()

filtered_divisor, result = kasiski_analysis(cipher_text, sequence_length=3)

if isinstance(result, str):
    print(result)
else:
    print(f"Ймовірна довжина ключа: {filtered_divisor}")
    print("Інші ймовірні результати")
    for length, frequency in result[:10]:
        print(f"Довжина: {length}, Частота: {frequency}")

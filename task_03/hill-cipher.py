'''Реалізація шифру Гілла, як прикладу табличного шифру'''

from math import gcd
import re
import numpy as np


def text_to_numbers(text):
    '''Перетворює текст у числа (A=0, B=1, ..., Z=25).'''
    return [ord(char) - ord('A') for char in text]


def numbers_to_text(numbers):
    '''Перетворює числа у текст.'''
    return ''.join(chr(num + ord('A')) for num in numbers)


def generate_key_matrix(block_size, modulus=26, keyword="MATRIX"):
    """Генерує верхньо-трикутну обернену матрицю із значеннями ключа."""
    matrix = np.zeros((block_size, block_size), dtype=int)
    keyword_numbers = text_to_numbers(keyword)

    # Розширюємо або обрізаємо keyword_numbers до потрібного розміру
    # Кількість елементів верхнього трикутника
    upper_triangle_size = (block_size * (block_size - 1)) // 2
    while len(keyword_numbers) < upper_triangle_size:
        keyword_numbers += keyword_numbers[:upper_triangle_size -
                                           len(keyword_numbers)]
    keyword_numbers = keyword_numbers[:upper_triangle_size]

    # Використовуємо суму keyword_numbers як seed
    np.random.seed(sum(keyword_numbers))

    # Заповнюємо діагональ та верхній трикутник
    index = 0
    for i in range(block_size):
        # Елементи на діагоналі вибираємо так, щоб вони були взаємно простими із модулем
        while True:
            diag_element = np.random.randint(1, modulus)
            if gcd(diag_element, modulus) == 1:
                break
        matrix[i, i] = diag_element

        # Заповнюємо верхній трикутник значеннями з keyword_numbers
        for j in range(i + 1, block_size):
            matrix[i, j] = keyword_numbers[index]
            index += 1

    return matrix


def split_blocks(numbers, block_size):
    '''Розбиває список чисел на блоки заданого розміру.'''
    blocks = []
    for i in range(0, len(numbers), block_size):
        block = numbers[i:i + block_size]
        if len(block) < block_size:
            block += [0] * (block_size - len(block))  # Доповнюємо нулями
        blocks.append(block)
    return blocks


def encrypt(plain_text, key_matrix):
    '''Шифрує текст за допомогою шифру Гілла.'''
    block_size = len(key_matrix)
    numbers = text_to_numbers(plain_text)
    blocks = split_blocks(numbers, block_size)

    encrypted_numbers = []
    for block in blocks:
        vector = np.array(block).reshape(-1, 1)
        encrypted_vector = np.dot(key_matrix, vector) % 26
        encrypted_numbers.extend(encrypted_vector.flatten())

    return numbers_to_text(encrypted_numbers)


def mod_matrix_inverse(matrix, modulus=26):
    """
    Обчислює обернену матрицю за модулем.

    matrix: квадратна матриця NumPy.
    modulus: модуль, за яким виконується обчислення.
    """
    size = len(matrix)

    # Обчислюємо визначник матриці
    determinant = int(round(np.linalg.det(matrix))) % modulus
    if gcd(determinant, modulus) != 1:
        raise ValueError(f"Матриця не має оберненої за модулем {modulus}.")

    # Знаходимо мультиплікативне обернення визначника
    determinant_inv = pow(determinant, -1, modulus)

    # Обчислюємо ад'юнктну матрицю
    adjugate_matrix = np.zeros((size, size), dtype=int)
    for i in range(size):
        for j in range(size):
            # Видаляємо рядок та стовпець
            minor = np.delete(np.delete(matrix, i, axis=0), j, axis=1)
            cofactor = ((-1) ** (i + j) *
                        int(round(np.linalg.det(minor)))) % modulus
            adjugate_matrix[j, i] = cofactor  # Транспонування

    # Обчислюємо обернену матрицю за модулем
    inverse_matrix = (determinant_inv * adjugate_matrix) % modulus

    return inverse_matrix


def decrypt(cipher_text, key_matrix):
    '''Дешифрує текст за допомогою шифру Гілла.'''
    block_size = len(key_matrix)
    numbers = text_to_numbers(cipher_text)
    blocks = split_blocks(numbers, block_size)

    # Обчислюємо обернену матрицю модулем 26
    inverse_matrix = mod_matrix_inverse(key_matrix, 26)
    # print(f"Обернена матриця:\n{inverse_matrix}")

    decrypted_numbers = []
    for block in blocks:
        vector = np.array(block).reshape(-1, 1)
        decrypted_vector = np.dot(inverse_matrix, vector) % 26
        decrypted_numbers.extend(decrypted_vector.flatten())

    return numbers_to_text(decrypted_numbers)


def main():

    BLOCK_SIZE = 5
    KEYWORD = "MATRIX"
    PLAINTEXT_FILE = 'plain_text.txt'
    CIPHERTEXT_FILE = 'task_03/cipher_text.txt'

    key_matrix = generate_key_matrix(block_size=BLOCK_SIZE, keyword=KEYWORD)
    print(f"Згенеровано ключову матрицю:\n{key_matrix}")

    print(f"\nЗчитую текст із файлу {PLAINTEXT_FILE}...")
    with open(PLAINTEXT_FILE, 'r', encoding='utf-8') as file:
        plaintext = file.read()

    plaintext = re.sub(r'[^A-Z ]', '', plaintext.upper())

    cipher_text = encrypt(plaintext, key_matrix)
    print("\nЗашифрований текст:", cipher_text)

    print(f"\nЗаписую зашифрований текст у файл {CIPHERTEXT_FILE}...")
    with open(CIPHERTEXT_FILE, 'w', encoding='utf-8') as file:
        file.write(cipher_text)

    decrypted_text = decrypt(cipher_text, key_matrix)
    print("\nРозшифрований текст:", decrypted_text)


if __name__ == '__main__':
    main()

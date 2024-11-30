'''Шифрування перестановкою'''
import re


def generate_permutation_key(key: str) -> list:
    '''Генерує порядок для перестановки на основі текстового ключа'''
    indexed_phrase = list(enumerate(key))
    sorted_phrase = sorted(indexed_phrase, key=lambda x: x[1])
    permutation_key = [index for index, _ in sorted_phrase]
    return permutation_key


def encrypt(plain_text, key):
    '''
    Шифрує текст на основі перестановки.

    plain_text: текст, який потрібно зашифрувати.
    key: ключ перестановки (список індексів).
    '''
    # Розбиваємо текст на блоки за довжиною ключа
    block_size = len(key)
    blocks = [plain_text[i:i + block_size]
              for i in range(0, len(plain_text), block_size)]

    # Переставляємо символи в кожному блоці відповідно до ключа
    encrypted_blocks = []
    for block in blocks:
        # Додаємо пробіли для неповних блоків
        block = block.ljust(block_size)
        encrypted_block = ''.join(block[key[i]] for i in range(len(key)))
        encrypted_blocks.append(encrypted_block)

    # Об'єднуємо блоки в зашифрований текст
    return ''.join(encrypted_blocks)


def decrypt(cipher_text, key):
    '''
    Дешифрує текст на основі перестановки.

    cipher_text: зашифрований текст.
    key: ключ перестановки (список індексів).
    '''
    # Розраховуємо довжину блоку
    block_size = len(key)
    blocks = [cipher_text[i:i + block_size]
              for i in range(0, len(cipher_text), block_size)]

    # Створюємо зворотний ключ (індекси для розшифрування)
    inverse_key = [key.index(i) for i in range(len(key))]

    # Дешифруємо кожен блок
    decrypted_blocks = []
    for block in blocks:
        decrypted_block = ''.join(block[inverse_key[i]]
                                  for i in range(len(inverse_key)))
        decrypted_blocks.append(decrypted_block)

    # Об'єднуємо блоки в розшифрований текст
    # Видаляємо можливі зайві пробіли
    return ''.join(decrypted_blocks).rstrip()


def main():

    PLAINTEXT_FILE = 'plain_text.txt'
    CIPHERTEXT_FILE = 'task_02/cipher_text.txt'
    KEY = "SECRET"

    print(f"Зчитую текст із файлу {PLAINTEXT_FILE}")
    with open(PLAINTEXT_FILE, 'r', encoding='utf-8') as file:
        plaintext = file.read()

    plaintext = re.sub(r'[^A-Z ]', '', plaintext.upper())

    print("Генерую порядок перестановки...")
    permutation_key = generate_permutation_key(KEY)
    print(f"Порядок перестановки {permutation_key}")

    print("Шифрую текст...")
    cipher_text = encrypt(plaintext, permutation_key)
    print(f"Зашифрований текст: \n {cipher_text}")

    print("\nРозшифровую текст...")
    decrypted_text = decrypt(cipher_text, permutation_key)
    print(f"Розшифрований текст: \n{decrypted_text}")

if __name__ == '__main__':
    main()

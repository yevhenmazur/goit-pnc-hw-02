'''Модуль виконує шифрування та розшифровку за алгоритмом Віженера. Результат складає у файл'''
import re

def extend_key(text, key):
    '''Якщо ключ коротший за plaintext, то розширити його до розміру plaintext'''
    key = list(key)
    if len(text) == len(key):
        return key
    else:
        for i in range(len(text) - len(key)):
            key.append(key[i % len(key)])
    return ''.join(key)


def vigenere_encrypt(text, key):
    '''Зашифрувати текст за допомогою шифру Віженера'''
    text = text.upper()
    key = extend_key(text, key.upper())
    cipher_text = []
    for i, char in enumerate(text):
        if char.isalpha():  # Лише літери обробляються
            x = (ord(char) + ord(key[i]) - 2 * ord('A')) % 26
            x += ord('A')
            cipher_text.append(chr(x))
        else:
            cipher_text.append(char)  # Інші символи додаються без змін
    return ''.join(cipher_text)


def vigenere_decrypt(cipher_text, key):
    '''Розшифрувати текст за допомогою шифру Віженера'''
    cipher_text = cipher_text.upper()
    key = extend_key(cipher_text, key.upper())
    original_text = []
    for i, char in enumerate(cipher_text):
        if char.isalpha():  # Лише літери обробляються
            x = (ord(char) - ord(key[i]) + 26) % 26
            x += ord('A')
            original_text.append(chr(x))
        else:
            original_text.append(char)  # Інші символи додаються без змін
    return ''.join(original_text)

# Використання
PLAINTEXT_FILE = 'plain_text.txt'
CIPHERTEXT_FILE = 'cipher_text.txt'
KEY = "CRYPTOGRAPHY"
# KEY = "ANYKEY"

print(f"Зчитую текст із файлу {PLAINTEXT_FILE}")
with open(PLAINTEXT_FILE, 'r', encoding='utf-8') as file:
    TEXT = file.read()

# Нормалізація тексту необхідна для коректної роботи тесту Касіскі.
# Шифрування і розшифровка працює і без неї.
TEXT = re.sub(r'[^A-Z]', '', TEXT.upper())

print("Застосовую шифрування")
ENCRYPTED_TEXT = vigenere_encrypt(TEXT, KEY)
print("Зашифрований текст:", ENCRYPTED_TEXT)
print(f"Записую зашифрований текст у файл {CIPHERTEXT_FILE}")
with open('cipher_text.txt', 'w', encoding='utf-8') as file:
    file.write(ENCRYPTED_TEXT)

print("Розшифровую текст для перевірки правильності роботи алгоритму")
DECRYPTED_TEXT = vigenere_decrypt(ENCRYPTED_TEXT, KEY)
print("Розшифрований текст:", DECRYPTED_TEXT)

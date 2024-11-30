'''Подвійне шифрування перестановкою'''
import re
from permutation import generate_permutation_key, encrypt, decrypt

def main():

    PLAINTEXT_FILE = 'plain_text.txt'
    KEY1 = "SECRET"
    KEY2 = "CRYPTO"

    print(f"Зчитую текст із файлу {PLAINTEXT_FILE}")
    with open(PLAINTEXT_FILE, 'r', encoding='utf-8') as file:
        plaintext = file.read()

    plaintext = re.sub(r'[^A-Z ]', '', plaintext.upper())

    print("Генерую порядки перестановки...")
    permutation_key1 = generate_permutation_key(KEY1)
    permutation_key2 = generate_permutation_key(KEY2)
    print(f"Порядок перестановки 1 {permutation_key1}")
    print(f"Порядок перестановки 2 {permutation_key2}")

    print("Шифрую текст...")
    cipher_text1 = encrypt(plaintext, permutation_key1)
    cipher_text2 = encrypt(cipher_text1, permutation_key2)
    print(f"Зашифрований текст: \n {cipher_text2}")

    print("\nРозшифровую текст...")
    decrypted_text1 = decrypt(cipher_text2, permutation_key2)
    decrypted_text = decrypt(decrypted_text1, permutation_key1)
    print(f"Розшифрований текст: \n{decrypted_text}")

if __name__ == '__main__':
    main()

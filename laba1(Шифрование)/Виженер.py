plaintext = input('Enter the word ')
keyword = input('Enter the keyword ')
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
keyword *= len(plaintext) // len(keyword) + 1


def encrypt_vigenere(plaintext, keyword):
    ciphertext = ''
    for i in range(len(plaintext)):
        index = alphabet.index(keyword[i])
        num = ord(plaintext[i])+index
        if 123 <= num <= 148:
            num += -26
        ciphertext += chr(num)
    return ciphertext
print(encrypt_vigenere(plaintext, keyword))

ciphertext = input('Enter the word ')
keyword = input('Enter the keyword ')
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
keyword *= len(ciphertext) // len(keyword) + 1


def encrypt_vigenere(ciphertext, keyword):
    plaintext = ''
    for i in range(len(ciphertext)):
        index = alphabet.index(keyword[i])
        num = ord(ciphertext[i])-index
        if 71 <= num <= 96:
            num += 26
        plaintext += chr(num)
    return plaintext
print(encrypt_vigenere(ciphertext, keyword))

plaintext = input('Enter the word ')


def encrypt_caesar(plaintext):
    ciphertext = ''
    for i in range(len(plaintext)):
        num = ord(plaintext[i])
        if 120 <= num <= 122 or 88 <= num <= 90:
            num += -23
        elif 97 <= num <= 119 or 65 <= num <= 87:
            num += 3
        ciphertext += chr(num)
    return ciphertext
print(encrypt_caesar(plaintext))

ciphertext = input('Enter the word ')


def encrypt_caesar(ciphertext):
    plaintext = ''
    for i in range(len(ciphertext)):
        num = ord(ciphertext[i])
        if 97 <= num <= 99 or 65 <= num <= 67:
            num += 23
        elif 100 <= num <= 122 or 68 <= num <= 90:
            num += -3
        plaintext += chr(num)
    return plaintext
print(encrypt_caesar(ciphertext))

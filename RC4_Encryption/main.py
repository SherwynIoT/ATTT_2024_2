def ksa(key):
    """Key Scheduling Algorithm (KSA)"""
    key_length = len(key)
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % key_length]) % 256
        S[i], S[j] = S[j], S[i]
    return S

def prga(S, text_length):
    """Pseudo-Random Generation Algorithm (PRGA)"""
    i = 0
    j = 0
    keystream = []
    for _ in range(text_length):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        keystream.append(K)
    return keystream

def rc4_encrypt(plaintext, key):
    """RC4 Encryption"""
    key = [ord(c) for c in key]
    S = ksa(key)
    keystream = prga(S, len(plaintext))
    ciphertext = [ord(c) ^ k for c, k in zip(plaintext, keystream)]
    return keystream, ciphertext

def main():
    plaintext = "Hanoi University of Science and Technology"
    key = "secretkey"  # Khóa bí mật tự định nghĩa

    keystream, ciphertext = rc4_encrypt(plaintext, key)

    print("Keystream (dòng khóa):")
    print(keystream)

    print("\nCiphertext (giá trị bản mã - dạng số):")
    print(ciphertext)

    print("\nCiphertext (giá trị bản mã - dạng hex):")
    print(' '.join(format(c, '02x') for c in ciphertext))

if __name__ == "__main__":
    main()
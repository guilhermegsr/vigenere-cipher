import string

class VigenereCipher:
    def __init__(self, key: str):
        self._key = self._validate_key(key)
        self._alphabet = string.ascii_uppercase
        self._mod = len(self._alphabet)

    def _validate_key(self, key: str) -> str:
        """
        Validates that the key contains only alphabetic characters (A-Z or a-z).
        Raises ValueError or TypeError for invalid keys.
        """
        if not isinstance(key, str):
            raise TypeError("Key must be a string.")

        if not key.isalpha():
            raise ValueError("Key must contain only alphabetic characters (A-Z or a-z).")

        return key.upper()

    def _extend_key(self, text: str) -> str:
        """
        Extends the key to match the number of alphabetic characters in the text.
        Non-alphabetic characters are ignored in this process.
        """
        filtered_text_length = len([c for c in text if c.isalpha()])
        extended_key = (self._key * (filtered_text_length // len(self._key) + 1))[:filtered_text_length]
        return extended_key

    def encrypt(self, plaintext: str) -> str:
        """
        Encrypts the plaintext using the Vigenère cipher.
        Non-alphabetic characters are preserved without modification.
        """
        key = self._extend_key(plaintext)
        ciphertext = []
        key_index = 0

        for char in plaintext:
            if char.isalpha():
                p_idx = ord(char.upper()) - ord('A')
                k_idx = ord(key[key_index]) - ord('A')
                c_idx = (p_idx + k_idx) % self._mod
                cipher_char = self._alphabet[c_idx]
                ciphertext.append(cipher_char)
                key_index += 1
            else:
                ciphertext.append(char)
        return ''.join(ciphertext)

    def decrypt(self, ciphertext: str) -> str:
        """
        Decrypts the ciphertext using the Vigenère cipher.
        Non-alphabetic characters are preserved without modification.
        """
        key = self._extend_key(ciphertext)
        plaintext = []
        key_index = 0

        for char in ciphertext:
            if char.isalpha():
                c_idx = ord(char.upper()) - ord('A')
                k_idx = ord(key[key_index]) - ord('A')
                p_idx = (c_idx - k_idx + self._mod) % self._mod
                plain_char = self._alphabet[p_idx]
                plaintext.append(plain_char)
                key_index += 1
            else:
                plaintext.append(char)
        return ''.join(plaintext)

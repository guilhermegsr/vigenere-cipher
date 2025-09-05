from crypto.vigenere import VigenereCipher

cipher = VigenereCipher("LEMON")

text = "HELLO WORLD!"
encrypted = cipher.encrypt(text)
decrypted = cipher.decrypt(encrypted)

print("Original :", text)
print("Encrypted:", encrypted)
print("Decrypted:", decrypted)

import pytest
from crypto.vigenere import VigenereCipher

# --- Basic functional tests ---

def test_encrypt_basic():
    cipher = VigenereCipher("LEMON")
    plaintext = "ATTACKATDAWN"
    assert cipher.encrypt(plaintext) == "LXFOPVEFRNHR"

def test_decrypt_basic():
    cipher = VigenereCipher("LEMON")
    ciphertext = "LXFOPVEFRNHR"
    assert cipher.decrypt(ciphertext) == "ATTACKATDAWN"

def test_encrypt_lowercase_input():
    cipher = VigenereCipher("LEMON")
    assert cipher.encrypt("attackatdawn") == "LXFOPVEFRNHR"

def test_decrypt_with_mixed_case():
    cipher = VigenereCipher("LEMON")
    assert cipher.decrypt("LxFoPvEfRnHr") == "ATTACKATDAWN"

# --- Input cleaning and formatting ---

def test_encrypt_with_spaces_and_punctuation():
    cipher = VigenereCipher("LEMON")
    plaintext = "Attack at dawn!!!"
    # Spaces and punctuation should be preserved
    assert cipher.encrypt(plaintext) == "LXFOPV EF RNHR!!!"

def test_decrypt_with_spaces_and_punctuation():
    cipher = VigenereCipher("LEMON")
    ciphertext = "LXFOPV EF RNHR!!!"
    assert cipher.decrypt(ciphertext) == "ATTACK AT DAWN!!!"

# --- Key validation ---

def test_key_with_non_alpha_characters_raises_value_error():
    with pytest.raises(ValueError):
        VigenereCipher("L3M0N!")

def test_key_all_lowercase():
    cipher = VigenereCipher("lemon")
    assert cipher.encrypt("ATTACKATDAWN") == "LXFOPVEFRNHR"

def test_empty_key_raises_value_error():
    with pytest.raises(ValueError):
        VigenereCipher("")

def test_key_with_only_non_letters_raises_value_error():
    with pytest.raises(ValueError):
        VigenereCipher("12345")

def test_key_with_wrong_type_raises_type_error():
    with pytest.raises(TypeError):
        VigenereCipher(123)

# --- Edge cases ---

def test_encrypt_single_letter():
    cipher = VigenereCipher("B")
    assert cipher.encrypt("A") == "B"

def test_decrypt_single_letter():
    cipher = VigenereCipher("B")
    assert cipher.decrypt("B") == "A"

def test_encrypt_decrypt_full_alphabet():
    cipher = VigenereCipher("KEY")
    text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    encrypted = cipher.encrypt(text)
    decrypted = cipher.decrypt(encrypted)
    assert decrypted == text

def test_encrypt_empty_string():
    cipher = VigenereCipher("LEMON")
    assert cipher.encrypt("") == ""

def test_decrypt_empty_string():
    cipher = VigenereCipher("LEMON")
    assert cipher.decrypt("") == ""

def test_encrypt_long_key():
    cipher = VigenereCipher("SUPERCALIFRAGILISTICEXPIALIDOCIOUS")
    # Just check it runs without error
    result = cipher.encrypt("HELLO")
    assert isinstance(result, str) and len(result) == 5

def test_decrypt_matches_original():
    cipher = VigenereCipher("KEY")
    text = "TheQuickBrownFoxJumpsOverTheLazyDog"
    encrypted = cipher.encrypt(text)
    decrypted = cipher.decrypt(encrypted)
    assert decrypted == "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG"

# --- Regression test: short key with long message ---

def test_long_plaintext_short_key():
    cipher = VigenereCipher("A")
    plaintext = "THISISALONGMESSAGE"
    # Key 'A' = shift 0 → text unchanged
    assert cipher.encrypt(plaintext) == plaintext

def test_long_plaintext_key_B():
    cipher = VigenereCipher("B")
    plaintext = "THISISALONGMESSAGE"
    expected = "".join(
        chr(((ord(c) - 65 + 1) % 26) + 65) for c in plaintext
    )
    assert cipher.encrypt(plaintext) == expected

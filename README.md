# Vigenère Cipher in Python

This project contains an implementation of the **Vigenère cipher** in Python, along with a comprehensive test suite using `pytest`.

## 📖 About

The Vigenère cipher is a method of encrypting alphabetic text by using a series of Caesar ciphers based on the letters of a key.  
This implementation:

- Supports both **encryption** and **decryption**.
- Preserves **spaces, punctuation, and numbers** (non-alphabetic characters are not encrypted).
- Accepts keys with **alphabetic characters only** (A–Z, a–z).
- Converts all output to **uppercase** for consistency.
from crypto.vigenere import VigenereCipher
from analyser.vigenere_analyser import VigenereAnalyser

cipher = VigenereCipher("BOI")

text = "Technology has changed the way we live, work, and interact with the world around us." \
"From the moment we wake up and check our phones to the time we go to bed, technology plays an essential role in our daily routines." \
"It connects us with people across the globe, gives us instant access to information, and helps automate countless tasks." \
"While some argue that it makes us overly dependent or less social, others believe it creates new opportunities for learning and growth." \
"The rise of artificial intelligence, for example, has transformed industries such as healthcare, finance, and education." \
"Robots can now perform surgeries, algorithms can detect fraud, and online platforms can personalize learning for students." \
"However, with great power comes great responsibility." \
"It is important to consider privacy, data security, and ethical concerns." \
"As technology continues to evolve, we must ensure that its development benefits all of humanity and not just a select few."

encrypted = cipher.encrypt(text)
decrypted = cipher.decrypt(encrypted)

print("Original :", text)
print("Encrypted:", encrypted)
print("Decrypted:", decrypted)

analyser = VigenereAnalyser(encrypted, language="en")
key = analyser.analyse(max_len=10)

print("KEY:", key)
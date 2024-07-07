
import time

print("Carregando o modelo na RAM...")
now = time.time()

from transformers import pipeline
classifier = pipeline("text-classification", model="michellejieli/emotion_text_classifier", top_k=2)


print("Tempo de carregamento: ", (time.time() - now))
print("Aguardando 5s...")
time.sleep(5)

now = time.time()
frase = "Hi Fred! How are you?"
print(frase, ":", classifier(frase))
print("Elapsed time: ", (time.time() - now))

now = time.time()
frase = "Hey Frida! I'm fine and you?"
print(frase, ":", classifier(frase))
print("Elapsed time: ", (time.time() - now))

now = time.time()
frase = "I'm so sad... I've lost my cell phone..."
print(frase, ":", classifier(frase))
print("Elapsed time: ", (time.time() - now))

now = time.time()
frase = "oh... so sorry for you..."
print(frase, ":", classifier(frase))
print("Elapsed time: ", (time.time() - now))

now = time.time()
frase = "I need to buy another one. Can you help me on that?"
print(frase, ":", classifier(frase))
print("Elapsed time: ", (time.time() - now))

now = time.time()
frase = "Sure! I'll be happy to help you!"
print(frase, ":", classifier(frase))
print("Elapsed time: ", (time.time() - now))

now = time.time()
frase = "Thank you very much! See you tomorrow!"
print(frase, ":", classifier(frase))
print("Elapsed time: ", (time.time() - now))

print("Aguardando 5s...")
time.sleep(5)




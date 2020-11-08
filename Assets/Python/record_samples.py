import voice_processing.microphone as mic
import os
import keyboard
import time

path = input("Digite o identificador da amostra: ")
i = int(input("Digite o numero inicial da amostra: ") or 0)

input("Pressione qualquer tecla para iniciar a gravação")
while True:
    mic.recordToFile("sounds/{}/output_{}.wav".format(path, i))
    print("Amostra {} gravada".format(i))
    input("Pressione qualquer tecla para continuar")
    i = i + 1

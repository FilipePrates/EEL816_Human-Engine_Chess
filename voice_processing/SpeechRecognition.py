from dtw import *
from fastdtw import fastdtw
import numpy as np
import librosa
from copy import deepcopy

class SpeechReconizer:
    def __init__(self, labelsPath):
        # Inicializa o objeto de reconhecimento.
        # Usa o caminho 'labelsPath' para obter uma lista
        # dos rótulos passiveis de reconhecimento.
        with open(labelsPath) as f:
            labels = np.array([l.replace('\n', '') for l in f.readlines()])
        self.labels = labels
        self.callbacks = {}
       
       
    def recognize(self, audioStream, executeCallback = False):
        # Executa a rotina de reconhecimento e retorna o rótulo associado.
        # Se 'executeCallback' for igual True, o callback associado a esse rótulo será chamado.
        pass

    def attachCallback(self, label, callback):
        # Vincula uma chamada de callback ao rótulo passado em 'label'.
        if label in self.callbacks:
            print("Esse label já tem um callback definido")
            return

        self.callbacks[label] = callback

    def attachDefaultCallback(self, callback):
        # Vincula uma chamada de callback padrão.
        # É usada caso o audio não tenha sido reconhecido.
        self.defaultCallback = callback

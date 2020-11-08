import numpy as np
import librosa
from copy import deepcopy
import glob, os        
from .SpeechRecognition import SpeechReconizer
from pydtw import dtw1d, dtw2d

class PyDtwSpeechReconizer(SpeechReconizer):
    def __init__(self, labelsPath, tolerance, maxTolerance, k):
        super().__init__(labelsPath, tolerance, maxTolerance, k)
        self.precomputeMFCCs()
        pass
        
    def __reconizer_run(self, x, y):
        """
        Roda o algotimo com a função de distância escolhida.
        
        Esse método pode ser sobrescrito para utilizar implementações diferentes do DTW.
        Como o AcceleratedDTW.
        """
        return dtw1d(x, y).get_dist()
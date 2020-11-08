# -*- coding: utf-8 -*-
from fastdtw import fastdtw
import numpy as np
import librosa
from copy import deepcopy
import glob, os        
from .SpeechRecognition import SpeechReconizer

class FastDtwSpeechReconizer(SpeechReconizer):
    def __init__(self, labelsPath, tolerance, maxTolerance, k, distFunction = lambda x, y: np.linalg.norm(x - y, ord = 1)):
        super().__init__(labelsPath, tolerance, maxTolerance, k)
        self.distFunction = distFunction
        self.precomputeMFCCs()
        pass
        
    def _reconizer_run(self, x, y):
        """
        Roda o algotimo com a função de distância escolhida.
        
        Esse método pode ser sobrescrito para utilizar implementações diferentes do DTW.
        Como o AcceleratedDTW.
        """
        return fastdtw(x, y, dist = 1)
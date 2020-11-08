# -*- coding: utf-8 -*-
import numpy as np
from .SpeechRecognition import SpeechReconizer
from cydtw import dtw

class CyDtwSpeechReconizer(SpeechReconizer):
    def __init__(self, labelsPath, tolerance, maxTolerance, k):
        super().__init__(labelsPath, tolerance, maxTolerance, k)
        pass
        
    def _reconizer_run(self, x, y):
        """
        Roda o algotimo com a função de distância escolhida.
        
        Esse método pode ser sobrescrito para utilizar implementações diferentes do DTW.
        Como o AcceleratedDTW.
        """
        return dtw(x, y)

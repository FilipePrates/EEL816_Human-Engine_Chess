import numpy as np
import librosa
from copy import deepcopy
import glob, os        
from .SpeechRecognition import SpeechReconizer
from cydtw import dtw

class CyDtwSpeechReconizer(SpeechReconizer):
    def __init__(self, labelsPath, tolerance, maxTolerance):
        super().__init__(labelsPath, tolerance, maxTolerance)
        self.precomputeMFCCs()
        pass
        
    def _DtwSpeechReconizer__run(self, x, y):
        """
        Roda o algotimo com a função de distância escolhida.
        
        Esse método pode ser sobrescrito para utilizar implementações diferentes do DTW.
        Como o AcceleratedDTW.
        """
        return dtw(x, y)

    def __recognize(self, audioStream, executeCallback = False):
        """
        Faz reconhecimento da stream de audio usando alguma implementação do algoritmo FastDTW
        """
        x = self.__computeMFCC(audioStream)
        currentMinDist, currentMinId = np.inf, -1
        dist = float('inf')
        for i, y in self.mfccs.items():
            dist = self._DtwSpeechReconizer__run(x, y)

            if dist < currentMinDist:
                currentMinDist = dist
                currentMinId = i
            if dist < self.tolerance:
                break
        pass

        if dist > self.maxTolerance:
            self.failedCallback()
            return (False, None, None, None)

        label = self.labels[currentMinId]        
        if executeCallback:
            if label in self.callbacks:
                self.callbacks[label](label, currentMinDist, self.samples[currentMinId])
            else:
                self.defaultCallback(label, currentMinDist, self.samples[currentMinId])

        return (True, label, currentMinDist, self.samples[currentMinId])
            
    def recognizeFile(self, audioPath, executeCallback = False):
        """
        Faz reconhecimento do arquivo de audio usando alguma implementação do algoritmo FastDTW
        """
        return self.__recognize(librosa.load(audioPath), executeCallback)
    
    def recognize(self, audioStream, executeCallback = False):
        """
        Faz reconhecimento do arquivo de audio usando alguma implementação do algoritmo FastDTW
        """
        return self.__recognize(audioStream, executeCallback)

    def precomputeMFCCs(self):
        """
        Pre computa MFCCs dos audios salvos para agilizar o reconhecimento.
        """
        self.mfccs = {}
        self.samples = {}
        for i in range(len(self.labels)):
            label = self.labels[i]
            directory = 'sounds/{}/'.format(label)
            for filename in os.listdir(directory):
                if not filename.endswith(".wav"):
                    continue

                audio = librosa.load('{}/{}'.format(directory, filename))
                self.samples[i] = audio
                self.mfccs[i] = self.__computeMFCC(audio)
            pass
        pass
        
    def __computeMFCC(self, audio, normalize = True):
        """
        Computa MFCC e normaliza valores do audio passado.
        """
        y, sr = audio
        #return y #np.array(y, dtype = np.float64)

        mfcc = librosa.feature.mfcc(y, sr)

        if not normalize:
            return mfcc.T, audio
        
        mfcc_cp = deepcopy(mfcc)
        for j in range(mfcc.shape[1]):
            mfcc_cp[:, j] = mfcc[:, j] - np.mean(mfcc[:, j])
            mfcc_cp[:, j] = mfcc_cp[:, j]/np.max(np.abs(mfcc_cp[:, j]))
        pass

        return mfcc_cp.T.astype(np.float)
from fastdtw import fastdtw
import numpy as np
import librosa
from copy import deepcopy

class DtwSpeechReconizer(SpeechReconizer):
    def __init__(self, labelsPath, distFunction):
        super().__init(self, labelsPath)
        self.distFunction = distFunction
        pass
        
    def _DtwSpeechReconizer__run(self, x, y):
        """
        Roda o algotimo com a função de distância escolhida.
        
        Esse método pode ser sobrescrito para utilizar implementações diferentes do DTW.
        Como o AcceleratedDTW.
        """
        return fastdtw(x, y, dist = self.distFunction)
                
    def recognize(self, audioStream, executeCallback = False):
        """
        Faz reconhecimento da stream de audio usando alguma implementação do algoritmo FastDTW
        """
        x, audio = self.__computeMFCC(librosa.load(audioFile))
        currentMinDist, currentMinId = np.inf, -1

        for i, y in self.mfccs.items():
            dist, _ = self._DtwSpeechReconizer__run(x, y)

            if dist < currentMinDist:
                currentMinDist = dist
                currentMinId = i
        
        label = self.labels[currentMinId]        
        if executeCallback:
            if label in self.callbacks:
                self.callbacks[label](label, currentMinDist, self.samples[currentMinId])
            else:
                self.defaultCallback(label, currentMinDist, self.samples[currentMinId])

        return label, currentMinDist, self.samples[currentMinId]

    def precomputeMFCCs(self):
        """
        Pre computa MFCCs dos audios salvos para agilizar o reconhecimento.
        """
        self.mfccs = {}
        self.samples = {}
        for i in range(len(self.labels)):
            audio = librosa.load('sounds/{}.wav'.format(i))
            self.mfccs[i], self.samples[i] = self.__computeMFCC(audio)
        pass
        
    def __computeMFCC(self, audio, normalize = True):
        """
        Computa MFCC e normaliza valores do audio passado.
        """
        y, sr = audio
        mfcc = librosa.feature.mfcc(y, sr)

        if not normalize:
            return mfcc.T, audio
        
        mfcc_cp = deepcopy(mfcc)
        for j in range(mfcc.shape[1]):
            mfcc_cp[:, j] = mfcc[:, j] - np.mean(mfcc[:, j])
            mfcc_cp[:, j] = mfcc_cp[:, j]/np.max(np.abs(mfcc_cp[:, j]))
        
        return mfcc_cp.T, audio
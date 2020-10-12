from fastdtw import fastdtw
import numpy as np
import librosa
from copy import deepcopy
import glob, os        

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


class DtwSpeechReconizer(SpeechReconizer):
    def __init__(self, labelsPath, distFunction = np.linalg.norm):
        super().__init__(labelsPath)
        self.distFunction = distFunction
        self.precomputeMFCCs()
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
        x = self.__computeMFCC(librosa.load(audioStream))
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
        mfcc = librosa.feature.mfcc(y, sr)

        if not normalize:
            return mfcc.T, audio
        
        mfcc_cp = deepcopy(mfcc)
        for j in range(mfcc.shape[1]):
            mfcc_cp[:, j] = mfcc[:, j] - np.mean(mfcc[:, j])
            mfcc_cp[:, j] = mfcc_cp[:, j]/np.max(np.abs(mfcc_cp[:, j]))
        
        return mfcc_cp.T
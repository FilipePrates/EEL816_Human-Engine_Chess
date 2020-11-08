# -*- coding: utf-8 -*-
import numpy as np
import librosa
from copy import deepcopy
import glob, os
import shutil
from scipy.cluster.vq import vq, kmeans, kmeans2, whiten

def safe_copy(file_path, out_dir, dst = None):
    """Safely copy a file to the specified directory. If a file with the same name already 
    exists, the copied file name is altered to preserve both.

    :param str file_path: Path to the file to copy.
    :param str out_dir: Directory to copy the file into.
    :param str dst: New name for the copied file. If None, use the name of the original
        file.
    """
    name = dst or os.path.basename(file_path)
    if not os.path.exists(os.path.join(out_dir, name)):
        shutil.copy(file_path, os.path.join(out_dir, name))
    else:
        base, extension = os.path.splitext(name)
        i = 1
        while os.path.exists(os.path.join(out_dir, '{}_{}{}'.format(base, i, extension))):
            i += 1
        shutil.copy(file_path, os.path.join(out_dir, '{}_{}{}'.format(base, i, extension)))

class SpeechReconizer:
    def __init__(self, labelsPath, tolerance, maxTolerance, k):
        # Inicializa o objeto de reconhecimento.
        # Usa o caminho 'labelsPath' para obter uma lista
        # dos rótulos passiveis de reconhecimento.
        with open(labelsPath) as f:
            labels = np.array([l.replace('\n', '') for l in f.readlines()])
        self.labels = labels
        self.callbacks = {}
        self.tolerance = tolerance
        self.maxTolerance = maxTolerance
        self.allMfccs = {}
        self.mfccs = {}
        self.k = k
        self.precomputeMFCCs()
       
    def recognizeFile(self, audioPath, executeCallback = False):
        """
        Faz reconhecimento do arquivo de audio usando alguma implementação do algoritmo FastDTW
        """
        result = self.__recognize(librosa.load(audioPath), executeCallback)

        if (result[2] <= self.tolerance):
            self.mfccs[result[3]].append(result[4])
            dest = "sounds/" + result[1] + "/"
            print(dest)
            safe_copy(audioPath, dest)

        return result

    def __recognize(self, audioStream, executeCallback = False):
        """
        Faz reconhecimento da stream de audio
        """
        x = self._computeMFCC(audioStream)
        currentMinDist, currentMinId = np.inf, -1
        dist = float('inf')
        for i in range(len(self.labels)):
            label = self.labels[i]
            for y in self.mfccs[i]:
                dist = self._reconizer_run(x, y)

                if dist > currentMinDist:
                    continue
                
                currentMinDist = dist
                currentMinId = i
                if dist <= self.tolerance:
                    break
            pass
        pass

        if dist > self.maxTolerance:
            self.failedCallback()
            return (False, None, float('inf'), None, None)

        label = self.labels[currentMinId]        
        if executeCallback:
            if label in self.callbacks:
                self.callbacks[label](label, currentMinDist)
            else:
                self.defaultCallback(label, currentMinDist)
        
        return (True, label, currentMinDist, currentMinId, x)
        
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

    def attachFailedCallback(self, callback):
        # Vincula uma chamada de callback padrão.
        # É usada caso o audio não tenha sido reconhecido.
        self.failedCallback = callback

    def precomputeMFCCs(self):
        """
        Pre computa MFCCs dos audios salvos para agilizar o reconhecimento.
        """
        for i in range(len(self.labels)):
            label = self.labels[i]
            directory = 'sounds/{}/'.format(label)
            mfccs = []
            for filename in os.listdir(directory):
                if not filename.endswith(".wav"):
                    continue

                audio = librosa.load('{}/{}'.format(directory, filename))
                mfccs.append(self._computeMFCC(audio))
            pass
            self.allMfccs[i] = mfccs
        pass
        self.extractMostSignificant()

    def extractMostSignificant(self):
        for i in range(len(self.labels)):
            # print(self.allMfccs[i])
            self.mfccs[i] = self.allMfccs[i] #kmeans2(self.allMfccs[i], self.k) 
            # print(self.mfccs[i])
        pass


    def _computeMFCC(self, audio, normalize = True):
        """
        Computa MFCC e normaliza valores do audio passado.
        """
        y, sr = audio

        mfcc = librosa.feature.mfcc(y, sr).astype(np.float)
        if not normalize:
            return mfcc.T
        
        mfcc_cp = deepcopy(mfcc)
        for j in range(mfcc.shape[1]):
            mfcc_cp[:, j] = mfcc[:, j] - np.mean(mfcc[:, j])
            mfcc_cp[:, j] = mfcc_cp[:, j]/np.max(np.abs(mfcc_cp[:, j]))
        pass
        return mfcc_cp.T

    def _reconizer_run(self, x, y):
        raise Exception("Not implemented")

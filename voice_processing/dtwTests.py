import dtwSpeechRecognition as sr
from random import shuffle
from matplotlib import pyplot as plt

def orderedSet(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

def generateTrainTestSet(self, P):
    """Seleciona P amostras de audio para compor o conjunto de
        teste e as demais para o treinamento"""
    train = []
    test = []

    for s in orderedSet(self.labels):
        all = [i for i in range(len(self.labels)) if self.labels[i] == s]
        #shuffle(all)
        train += all[:-P]
        test += all[-P:]
    return train, test

    
def crossValidation(train, test, labels, mfccs, samples):
    score = 0.0
    trainMFCCs = [mfccs[i] for i in train]
    
    for i in test:
        recId, recDist = recognize(mfccs[i], trainMFCCs)
        recId = train[recId]
        
        correct = labels[i] == labels[recId]
        print(recDist, i, labels[i], recId, labels[recId], correct)
        if (correct):
            score += 1.0
        else:
            pass
        
    return score / len(test)



recognizer = DtwSpeechReconizer("sounds/labels.txt", lambda a, b: np.linalg.norm(a - b, ord=1))

labels = loadLabels()
train, test = generateTrainTestSet(labels, 1)
mfccs, samples = precomputeMFCCs(labels)


rec_rate = crossValidation(train, test, labels, mfccs, samples)
print ('Recognition rate {}%'.format(100. * rec_rate))

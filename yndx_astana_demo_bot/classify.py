#train_models.py

import os
from glob import glob
import cPickle

import numpy as np
from scipy.io.wavfile import read
from sklearn.mixture import GMM 
from sklearn import preprocessing
import python_speech_features as mfcc

def is_male(f):
    models = []
    with open("male.gmm") as model:
        models.append( cPickle.load(model) )
    with open("female.gmm") as model:
        models.append( cPickle.load(model) )

    sr, audio  = read(f)
    features   = get_mfcc(sr,audio)
    scores     = None
    log_likelihood = np.zeros(len(models)) 
    for i, gmm in enumerate(models):
        scores = np.array(gmm.score(features))
        log_likelihood[i] = scores.sum()

    return np.argmax(log_likelihood) == 0


def get_mfcc(sr, audio):
    features = get_features(sr, audio)
    feat     = np.asarray(())
    for i in range(features.shape[0]):
        temp = features[i,:]
        if np.isnan(np.min(temp)):
            continue
        else:
            if feat.size == 0:
                feat = temp
            else:
                feat = np.vstack((feat, temp))
    features = feat;
    features = preprocessing.scale(features)
    return features


def get_features(sr, audio):
    return mfcc.mfcc(audio, sr, 0.025, 0.01, 13, appendEnergy=False, nfft=2048)


def save_wav(ogg, wav):
    os.system("ffmpeg -i {} -c:a pcm_f32le {}".format(ogg, wav))


def learn(files):
    features = np.asarray(());
    for f in files:
        sr,audio = read(f)
        vector = preprocessing.scale(get_features(sr, audio))
        if features.size == 0:
            features = vector
        else:
            features = np.vstack((features, vector))

    gmm = GMM(n_components=8, n_iter=200, covariance_type='diag', n_init=3)
    gmm.fit(features)
    return gmm


def male_voices():
    return glob("male-voice-*.wav")


def female_voices():
    return glob("female-voice-*.wav")


def refresh_gmm_models():
    with open("male.gmm", 'w') as model:
        cPickle.dump(learn(male_voices()), model)
    with open("female.gmm", 'w') as model:
        cPickle.dump(learn(female_voices()), model)


if __name__ == '__main__':
    refresh_gmm_models()


#train_models.py

import os
from glob import glob
import cPickle

import numpy as np
from scipy.io.wavfile import read
from sklearn.mixture import GMM 
from sklearn import preprocessing
import python_speech_features as mfcc

import warnings
warnings.filterwarnings('ignore', 'Class GMM is deprecated', DeprecationWarning)
warnings.filterwarnings('ignore', 'Function distribute_covar_matrix_to_match_covariance_type is deprecated', DeprecationWarning)
warnings.filterwarnings('ignore', 'Function log_multivariate_normal_density is deprecated', DeprecationWarning)


VOICES_DIR = 'voices'


def trained_models_exist():
    return os.path.exists("male.gmm") and os.path.exists("female.gmm")


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


def add_new_female_voice(fname):
    if not os.path.exists(VOICES_DIR):
        os.makedirs(VOICES_DIR)
    save_wav(fname, VOICES_DIR + "/female-{}.wav".format(os.path.basename(fname)))


def add_new_male_voice(fname):
    if not os.path.exists(VOICES_DIR):
        os.makedirs(VOICES_DIR)
    save_wav(fname, VOICES_DIR + "/male-{}.wav".format(os.path.basename(fname)))


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
    return glob(VOICES_DIR + "/male-*.wav")


def female_voices():
    return glob(VOICES_DIR + "/female-*.wav")


def refresh_gmm_models():
    male_voices_files = male_voices()
    if male_voices_files:
        with open("male.gmm", 'w') as model:
            cPickle.dump(learn(male_voices_files), model)

    female_voices_files = female_voices()
    if female_voices_files:
        with open("female.gmm", 'w') as model:
            cPickle.dump(learn(female_voices_files), model)


if __name__ == '__main__':
    refresh_gmm_models()


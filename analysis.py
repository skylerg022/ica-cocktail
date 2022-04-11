# -*- coding: utf-8 -*-

#%% load modules
from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
from os import listdir
import regex as re

from sklearn.decomposition import FastICA, PCA

#%% EDA: Observed audio from 5 mics

# files = ['S08_U01.CH1.wav', 'S08_U02.CH1.wav', 'S08_U03.CH1.wav', 
#          'S08_U04.CH1.wav', 'S08_U05.CH1.wav']
r = re.compile('.*CH7.*')
files = list(filter(r.match, listdir('./data/')))
n_files = len(files)

# Assuming that all mics have same sample size
_, audio = wavfile.read('./data/' + files[0])
n = len(audio)

# Visualize and save data into X matrix
X = np.empty((n, n_files))
for i in range(n_files):
    samplerate, audio = wavfile.read('./data/' + files[i])
    assert len(audio) == n, 'Sample size of ' + files[i] + ' is not the same as' + files[0] + '.'
    plt.plot(range(len(audio)), audio)
    plt.show()
    # input('Press [Enter] to continue...')
    X[:,i] = audio
# X /= X.std(axis = 0)

#%% EDA: Speaker audio

r = re.compile('.*P.*')
files = list(filter(r.match, listdir('./data/')))

for file in files:
    samplerate, audio = wavfile.read('./data/' + file)
    plt.plot(range(len(audio)), audio)
    plt.show()
    # input('Press [Enter] to continue...')


#%% Compute ICA
n_comp = 4
ica = FastICA(n_components = n_comp, random_state = 293)
S_ = ica.fit_transform(X)  # Reconstruct signals
A_ = ica.mixing_  # Get estimated mixing matrix

# We can `prove` that the ICA model applies by reverting the unmixing.
# assert np.allclose(X, np.dot(S_, A_.T) + ica.mean_)

# (X - (np.dot(S_, A_.T) + ica.mean_)).max()

# For comparison, compute PCA
pca = PCA(n_components = n_comp)
H = pca.fit_transform(X)  # Reconstruct signals based on orthogonal components

#%% Plot results

plt.figure()
name = "ICA recovered signals"
colors = ["red", "steelblue", "orange", "green", "purple"]
plt.title(name)
for ii, (sig, color) in enumerate(zip(S_.T, colors), 1):
    plt.subplot(n_comp, 1, ii)
    plt.plot(sig, color=color)
plt.show()



#%% Save output
S = np.int16(S_ / np.abs(S_).max(axis = 0) * 1200) # 32767)
H = np.int16(H / np.abs(H).max(axis = 0) * 1200) # 32767)
# result_signal_1_int = np.int16(result_signal_1*32767*100)

wavfile.write('data/out1.wav', samplerate, S[:,0])
wavfile.write('data/out2.wav', samplerate, S[:,1])
wavfile.write('data/out3.wav', samplerate, S[:,2])
wavfile.write('data/out4.wav', samplerate, S[:,3])
# wavfile.write('data/out5.wav', samplerate, S[:,4])

wavfile.write('data/pca_out1.wav', samplerate, H[:,0])
wavfile.write('data/pca_out2.wav', samplerate, H[:,1])
wavfile.write('data/pca_out3.wav', samplerate, H[:,2])
wavfile.write('data/pca_out4.wav', samplerate, H[:,3])
# wavfile.write('data/pca_out5.wav', samplerate, H[:,4])





# a = np.array([[2, 3, 5],
#               [-1, -1, -1],
#               [3, 3, 4],
#               [0, 0, 0]])
# amax = np.abs(a).max(axis = 0)
# a / amax

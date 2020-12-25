import numpy as np
import random

def addnoise_bw(seq, sampling_rate=1000):

  #===== gerate baseline wander noise =====#
  # set parameters (ref. BW Detection Threshold )
  F = random.choice([0.05, 0.1, 0.15, 0.2])   # No. of cycles per second, F = 500 Hz
  T = 10         # Time period, T = 2 ms
  Fs = sampling_rate   # No. of samples per second, Fs = 50 kHz
  Ts = 1./Fs       # Sampling interval, Ts = 20 us
  N = int(T/Ts)     # No. of samples for 2 ms, N = 100
  # generate
  t = np.linspace(0, T, N)
  noise = np.sin(2*np.pi*F*t)*0.1
  # add noise
  new_seq = seq + noise

  return new_seq


def addnoise_ma(seq):

  # random position
  new_ecg = seq.copy()
  num1 = np.random.randint(int(new_ecg.shape[0]*0.25), int(new_ecg.shape[0]*0.75))
  num2 = np.random.randint(int(new_ecg.shape[0]*0.25), int(new_ecg.shape[0]*0.75))
  _start = min([num1, num2])
  _end = max([num1, num2])

  # generate noise
  noise1 = np.random.randn(new_ecg[:_start].shape[0])*0.02
  #noise2 = np.random.randn(new_ecg[_start:_end].shape[0])*0.02
  noise3 = np.random.randn(new_ecg[_end:].shape[0])*0.02

  # update values
  new_ecg[:_start] += noise1
  #new_ecg[_start:_end] += noise2
  new_ecg[_end:] += noise3

  return new_ecg


def addnoise_gn(seq):

  new_ecg = seq.copy()
  noise = np.random.randn(new_ecg.shape[0])*0.02
  new_ecg += noise

  return new_ecg

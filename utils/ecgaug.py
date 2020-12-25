import neurokit2 as nk
import numpy as np


# peaks_detected
def peaks_detected(ecg, sampling_rate=1000):
    # R peak
    _, rpeaks = nk.ecg_peaks(ecg, sampling_rate=1000)
    # PQST peak
    signals, waves = nk.ecg_delineate(ecg, rpeaks,
                                      sampling_rate=1000, method='peak')
    # append all peaks
    peaks = {}
    peaks.update(rpeaks)
    peaks.update(waves)

    return peaks


# get segment
def get_segments(peaks, p1='ECG_R_Peaks', p2='ECG_T_Peaks'):
    p1_loc = peaks[p1]
    p2_loc = peaks[p2]

    # in case p1_loc[0] > p2_loc[0]
    if p1_loc[0] > p2_loc[0]:
        p1_loc = [int(x) for x in p1_loc[:-1]]
        p2_loc = [int(x) for x in p2_loc[1:]]
    else:
        p1_loc = [int(x) for x in p1_loc]
        p2_loc = [int(x) for x in p2_loc]

    # segment position
    segments = []
    for i, j in list(zip(p1_loc, p2_loc)):
        _seg = list(range(i, j))
        segments.append(_seg)

    return segments


# augmentation function
# slope
def segment_aug_slope(ecg, segments, frac=0.9):
    new_ecg = ecg.copy()
    # add slope
    for i in range(len(segments)):
        # generate linear slope
        length = int(len(ecg[segments[i]]) * frac)
        line = np.linspace(ecg[segments[i]][0] * 0.5, 0, num=length)

        # add linear to original data
        _aug = new_ecg[segments[i]]
        _aug[_aug.shape[0] - length:] += line

        new_ecg[segments[i]] = _aug

    return new_ecg


# flatten
def segment_aug_flatten(ecg, segments):
    new_ecg = ecg.copy()

    # flatten
    for i in range(len(segments)):
        _aug = new_ecg[segments[i]]
        _aug = _aug * 0.1

        new_ecg[segments[i]] = _aug

    return new_ecg

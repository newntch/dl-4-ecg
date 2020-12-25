from utils.ecgaug import *


def generate_ecg_v1(ecg, st_segments, tp_segments, pattern='normal', **kwargs):
    new_ecg = ecg.copy()
    # ===== augmentation =====#
    # flatten
    ecg_v1 = segment_aug_flatten(new_ecg, st_segments)
    ecg_v1 = segment_aug_flatten(ecg_v1, tp_segments)

    if pattern == 'normal':
        ecg_v1 = ecg_v1 * -1 * 0.3
        return ecg_v1
    else:
        rst_segments = kwargs.get('rst_segments', None)
        ecg_v1_ste = segment_aug_slope(ecg_v1, segments=rst_segments)
        ecg_v1_ste = ecg_v1_ste * -1 * 0.3
        return ecg_v1_ste


# ecg_v2 : decrease Q + flip_qrs
def generate_ecg_v2(ecg, q_peaks, qrs_segments, pattern='normal', **kwargs):
    new_ecg = ecg.copy()
    # ===== augmentation =====#
    # decrease Q
    _aug1 = new_ecg[q_peaks]
    _aug1 = _aug1 * 2
    new_ecg[q_peaks] = _aug1
    # flip_qrs
    for i in range(len(qrs_segments)):
        _aug2 = new_ecg[qrs_segments[i]]
        _aug2 = _aug2 * -1

        new_ecg[qrs_segments[i]] = _aug2

    # ===== pattern =====#
    if pattern == 'normal':
        ecg_v2 = new_ecg
        return ecg_v2
    else:
        rst_segments = kwargs.get('rst_segments', None)
        ecg_v2 = new_ecg
        ecg_v2_ste = segment_aug_slope(ecg_v2, segments=rst_segments)
        return ecg_v2_ste


# ecg_v3 : decrease Q + flip + scaled
def generate_ecg_v3(ecg, q_peaks, qrs_segments, pattern='normal', **kwargs):
    new_ecg = ecg.copy()
    # ===== augmentation =====#
    # decrease Q
    _aug1 = new_ecg[q_peaks]
    _aug1 = _aug1 * 2
    new_ecg[q_peaks] = _aug1
    # flip_qrs
    for i in range(len(qrs_segments)):
        _aug2 = new_ecg[qrs_segments[i]]
        _aug2 = _aug2 * -1

        new_ecg[qrs_segments[i]] = _aug2
    # scaled
    new_ecg = new_ecg * 0.5

    # ===== pattern =====#
    if pattern == 'normal':
        ecg_v3 = new_ecg
        return ecg_v3
    else:
        rst_segments = kwargs.get('rst_segments', None)
        ecg_v3 = new_ecg
        ecg_v3_ste = segment_aug_slope(ecg_v3, segments=rst_segments)
        return ecg_v3_ste


# ecg_v4 : decrease S + scaled
def generate_ecg_v4(ecg, pattern='normal', **kwargs):
    new_ecg = ecg.copy()
    # ===== augmentation =====#
    new_ecg = new_ecg * 0.5

    # ===== pattern =====#
    if pattern == 'normal':
        ecg_v4 = new_ecg
        return ecg_v4
    else:
        rst_segments = kwargs.get('rst_segments', None)
        ecg_v4 = new_ecg
        ecg_v4_ste = segment_aug_slope(ecg_v4, segments=rst_segments)
        return ecg_v4_ste

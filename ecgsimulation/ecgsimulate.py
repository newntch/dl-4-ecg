from utils.ecgnoise import *
from ecgsimulation.generate import *
import pandas as pd


# simulate dataset
def generate_ecg_dataset(pattern='normal', addnoise='none', n_samples=10):
  '''
    generate ECG dataset
    pattern : 'normal', 'ste'
    addnoise : 'none', 'bw', 'ma', 'gn'
    n_samples : number of samples
  '''

  #===== setting =====#
  duration = 10
  sampling_rate = 1000
  noise = 0
  method = 'ecgsyn'
  heart_rate = np.random.randint(60, 100)

  pattern = pattern
  addnoise = 'none'
  n_samples = n_samples

  #===== generate data =====#
  data = []
  for i in range(n_samples):
    ecg = nk.ecg_simulate(duration=duration,
                          sampling_rate=sampling_rate,
                          noise=noise,
                          heart_rate=heart_rate,
                          method=method)
    # get morphology
    peaks = peaks_detected(ecg, sampling_rate=1000)
    st_segments = get_segments(peaks, p1='ECG_S_Peaks', p2='ECG_T_Peaks')
    tp_segments = get_segments(peaks, p1='ECG_T_Peaks', p2='ECG_P_Peaks')
    q_peaks = peaks['ECG_Q_Peaks']
    qrs_segments = get_segments(peaks, p1='ECG_Q_Peaks', p2='ECG_S_Peaks')
    rst_segments = get_segments(peaks, p1='ECG_R_Peaks', p2='ECG_T_Peaks')
    # generate v1-v4
    if pattern == 'normal':
      v1 = generate_ecg_v1(ecg, st_segments, tp_segments, pattern=pattern)
      v2 = generate_ecg_v2(ecg, q_peaks, qrs_segments, pattern=pattern)
      v3 = generate_ecg_v3(ecg, q_peaks, qrs_segments, pattern=pattern)
      v4 = generate_ecg_v4(ecg, pattern=pattern)
    else :
      v1 = generate_ecg_v1(ecg, st_segments, tp_segments,
                          pattern='ste', rst_segments=rst_segments)
      v2 = generate_ecg_v2(ecg, q_peaks, qrs_segments,
                          pattern='ste', rst_segments=rst_segments)
      v3 = generate_ecg_v3(ecg, q_peaks, qrs_segments,
                          pattern='ste', rst_segments=rst_segments)
      v4 = generate_ecg_v4(ecg, pattern='ste', rst_segments=rst_segments)

    smp_data = {'id': i,
                'v1': v1[3001:6001],
                'v2': v2[3001:6001],
                'v3': v3[3001:6001],
                'v4': v4[3001:6001]}

    data.append(smp_data)

  # store data in DataFrame
  df = pd.DataFrame(data)

  # addnoise
  if addnoise == 'none':
    return df

  elif addnoise == 'bw':
    df_bw = df.apply(lambda x: addnoise_bw(x, sampling_rate=1000))
    return df_bw

  elif addnoise == 'ma':
    df_ma = df.apply(lambda x: addnoise_ma(x))
    return df_ma

  elif addnoise == 'gn':
    df_gn = df.apply(lambda x: addnoise_gn(x))
    return df_gn

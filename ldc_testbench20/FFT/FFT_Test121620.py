import matplotlib.pyplot as plt
import numpy as np
import warnings
import csv



RAW_SENSOR_FILE_NAME = r'201216093332.txt'
RAW_SENSOR_FILE_PATH = 'C:/Users/wadre/OneDrive/Desktop/WIT_Sensor/BWT901CL-20201207T194636Z-001/BWT901CL/Standard Software for Windows PC/Data/'



def fftPlot(sig, dt=None, plot=True):
    # here it's assumes analytic signal (real signal...)- so only half of the axis is required

    if dt is None:
        dt = 1
        t = np.arange(0, sig.shape[-1])
        xLabel = 'samples'
    else:
        t = np.arange(0, sig.shape[-1]) * dt
        xLabel = 'freq [Hz]'

    if sig.shape[0] % 2 != 0:
        warnings.warn("signal prefered to be even in size, autoFixing it...")
        t = t[0:-1]
        sig = sig[0:-1]

    sigFFT = np.fft.fft(sig) / t.shape[0]  # divided by size t for coherent magnitude

    freq = np.fft.fftfreq(t.shape[0], d=dt)

    # plot analytic signal - right half of freq axis needed only...
    firstNegInd = np.argmax(freq < 0)
    freqAxisPos = freq[0:firstNegInd]
    sigFFTPos = 2 * sigFFT[0:firstNegInd]  # *2 because of magnitude of analytic signal

    if plot:
        plt.figure()
        plt.plot(freqAxisPos, np.abs(sigFFTPos))
        plt.xlabel(xLabel)
        plt.ylabel('mag')
        plt.title('Analytic FFT plot')
        plt.show()

    return sigFFTPos, freqAxisPos


if __name__ == "__main__":

    raw_x_array = []
    raw_y_array = []
    raw_z_array = []

    with open(RAW_SENSOR_FILE_PATH + RAW_SENSOR_FILE_NAME, newline='') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            if (row[0] == '0x50'):
                raw_x_array.append(float(row[2]))
                raw_y_array.append(float(row[3]))
                raw_z_array.append(float(row[4]))

    sig = raw_x_array
    print(raw_x_array)
    dt = 1 / 100


    # build a signal within nyquist - the result will be the positive FFT with actual magnitude
    f0 = 200  # [Hz]
    t = np.arange(0, 1 + dt, dt)
    print (type(t))
    sig = 1 * np.sin(2 * np.pi * f0 * t) + \
        10 * np.sin(2 * np.pi * f0 / 2 * t) + \
        3 * np.sin(2 * np.pi * f0 / 4 * t) +\
        7.5 * np.sin(2 * np.pi * f0 / 5 * t)

    sig = np.array(raw_x_array)
    #print(sig)

    # res in freqs
    fftPlot(sig, dt=dt)
    # res in samples (if freqs axis is unknown)
    fftPlot(sig)
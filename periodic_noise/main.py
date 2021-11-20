import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

def get_spectrum(shifted):
    absolute = np.abs(shifted)
    min_val = np.amin(absolute)
    absolute[absolute == 0] = min_val
    spectrum = 35*np.log10(absolute)
    return spectrum, min_val


def DFFTnp(img, orig):
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    spectrum, min_val = get_spectrum(fshift)
    plt.subplot(141)
    plt.imshow(spectrum, cmap='gray', vmin=0, vmax=255)
    for a in fshift[0:337]: a[508:520] = min_val #320
    for a in fshift[345:]: a[508:520] = min_val
    for a in fshift[335:345]: a[0:508] = min_val #493
    for a in fshift[335:345]: a[515:] = min_val
    res, _ = get_spectrum(fshift)
    plt.subplot(142)
    plt.imshow(res, cmap='gray', vmin=0, vmax=255)

    final = np.real(np.fft.ifft2(np.fft.ifftshift(fshift)))
    plt.subplot(143)
    plt.imshow(final, cmap='gray', vmin=0, vmax=255)
    plt.subplot(144)
    plt.imshow(img, cmap='gray', vmin=0, vmax=255)
    plt.show()
    return fshift


image = cv.imread('./0.png', cv.IMREAD_GRAYSCALE)


n = np.float32(image)
DFFTnp(n, image)
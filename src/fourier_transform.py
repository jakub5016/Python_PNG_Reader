import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from skimage import io


def fft_transform_show(path):
    image = io.imread(path, as_gray=True)

    fft_image = np.fft.fft2(image)

    amplitude = np.abs(fft_image)
    shifted_amplitude = np.fft.fftshift(amplitude)
    phase = np.angle(fft_image)

    # Step 4: Plot the images
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 3, 1)
    plt.imshow(image, cmap="gray")
    plt.title("Original Image")
    plt.axis("off")

    plt.subplot(1, 3, 2)
    plt.imshow(shifted_amplitude, norm=LogNorm(vmin=5), cmap="gray")
    plt.title("Fourier Amplitude")
    plt.axis("off")

    plt.subplot(1, 3, 3)
    plt.imshow(phase, cmap="gray")
    plt.title("Fourier Phase")
    plt.axis("off")

    plt.tight_layout()
    plt.show()

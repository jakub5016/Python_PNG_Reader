from .hex_functions import delete_spaces_from_hex
import matplotlib.pyplot as plt
import numpy as np
import colorsys


def histogram(palette, hist_chunk):
    hist_data = delete_spaces_from_hex(hist_chunk[2])

    colors_rgb = [tuple(x) for x in palette]

    colors_brightness = []
    for item in colors_rgb:
        brightness = sum(item) / 3
        colors_brightness.append(brightness)

    colors_brightness.sort()

    fig, axs = plt.subplots(2, 2, figsize=(10, 8))

    axs[0, 0].hist(colors_brightness, bins=20, alpha=0.7, color="black")
    axs[0, 0].set_xticks(np.arange(0, 256, step=32))
    axs[0, 0].set_xlabel("Brightness")
    axs[0, 0].set_ylabel("Frequency")
    axs[0, 0].set_title("Histogram of Colors Brightness")

    for i, (component, color) in enumerate(
        zip(["Red", "Green", "Blue"], ["red", "green", "blue"])
    ):
        axs[(i + 1) // 2, (i + 1) % 2].hist(
            [color[i] for color in colors_rgb], bins=20, color=color, alpha=0.7
        )
        axs[(i + 1) // 2, (i + 1) % 2].set_xticks(np.arange(0, 256, step=32))
        axs[(i + 1) // 2, (i + 1) % 2].set_xlabel(f"{component} Intensity")
        axs[(i + 1) // 2, (i + 1) % 2].set_ylabel("Frequency")
        axs[(i + 1) // 2, (i + 1) % 2].set_title(f"Histogram of {component} Intensity")

    plt.tight_layout()
    plt.show()

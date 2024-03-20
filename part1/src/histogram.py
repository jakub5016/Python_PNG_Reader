from .hexFunctions import delete_spaces_from_hex
import matplotlib.pyplot as plt

def histogram(pallete, hist_chunk):
    hist_data = delete_spaces_from_hex(hist_chunk[2])

    colors_rgb = []
    for color in pallete:
        colors_rgb.append(tuple(x / 255.0 for x in color))

    frequency_array = []
    for frequency in range(0, len(hist_data), 2):
        frequency_array.append(int(hist_data[frequency] + hist_data[frequency+1], 16))
        
    
    n, bins, patches = plt.hist(frequency_array, bins=len(colors_rgb))

    for patch, color in zip(patches, colors_rgb):
        patch.set_facecolor(color)

    plt.title('Histogram with RGB Colors')
    plt.ylabel('Frequency')
    plt.show()

    # print(colors_rgb)

    # for frequency in hist_chunk:
    #     for color in pallete:

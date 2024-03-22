from .hexFunctions import delete_spaces_from_hex
import matplotlib.pyplot as plt
import colorsys
import math
def histogram(palette, hist_chunk):
    hist_data = delete_spaces_from_hex(hist_chunk[2])

    colors_rgb = []
    for color in palette:
        colors_rgb.append(tuple(x / 255.0 for x in color))

    colors_hls = [colorsys.rgb_to_hls(*rgb) for rgb in colors_rgb]

    sorted_indices = sorted(range(len(colors_hls)), key=lambda i: colors_hls[i][0])
    sorted_colors_rgb = [colors_rgb[i] for i in sorted_indices]
    sorted_colors_hex = [f'#{int(color[0]*255):02x}{int(color[1]*255):02x}{int(color[2]*255):02x}' for color in sorted_colors_rgb]
    
    frequency_array = []
    for frequency in range(0, len(hist_data), 2):
        frequency_array.append(int(hist_data[frequency], 16) + int(hist_data[frequency+1], 16))
    
    num_colors = min(len(frequency_array), len(sorted_colors_hex))
    plt.bar(range(num_colors), frequency_array[:num_colors], color=sorted_colors_rgb[:num_colors])
    
    plt.title('Bar Plot with Sorted Colors')
    plt.ylabel('Frequency')
    plt.xlabel('Color (RGB)')
    plt.xticks(range(num_colors), sorted_colors_hex[:num_colors], rotation=45)
    plt.show()

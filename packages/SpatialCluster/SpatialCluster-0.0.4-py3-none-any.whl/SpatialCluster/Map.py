import random
# Hernán: ver colores, estoy usando una paleta estática

import matplotlib.pyplot as plt
import matplotlib.colors as cl

COLORS = ['#ACE1AF', '#FFA700', 'yellow', 'orange', '#7CB9E8', '#A4C639',' green',
          '#DA1884', 'magenta', 'brown', 'blue', 'red', 'cyan', 'pink', '#BFFF00', '#FDEE00']

# Extraida de https://lospec.com/palette-list/oxygen-16 y se cambio el blanco por magenta
COLORS = ["magenta", "#f5d678", "#6be0bf", "#bab197", "#96d45b", "#f56c77", "#e0864a", "#59909e",
            "#9e4891", "#6e6660", "#505273", "#ab3737", "#693c36", "#3a363d", "#202026", "#579460"]

COLORS_9_SET = [plt.cm.Set1(i) for i in range(10)]
COLORS_9_SET = [cl.to_hex(c) for c in COLORS_9_SET]

import folium
from folium import Map

def visualize_map_sample(areas_to_points, clusters, min_supp, features, max_samples_per_clusters):
    hmap = Map(location=[-33.45, -70.65], control_scale=True, zoom_start=11, tiles = 'stamen toner')
    if len([x for x in areas_to_points.items() if len(x[1]) > min_supp]) <= 9:
        colors_to_use = COLORS_9_SET
    else:
        colors_to_use = COLORS
    sorted_points = {k: v for k, v in sorted(areas_to_points.items(), key=lambda item: len(item[1]), reverse=True)}
    
    for index, i in enumerate(sorted_points):
        if len(sorted_points[i]) <= min_supp:
            continue
        
        a_ = random.sample(sorted_points[i], min(len(sorted_points[i]), max_samples_per_clusters) )
        for point in a_:
            folium.Circle(location=[point[1], point[0]], popup = str(point),
                            color=colors_to_use[index], radius=10).add_to(hmap)
            
    return hmap
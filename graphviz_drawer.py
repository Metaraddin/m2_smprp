import graphviz
import numpy as np
import sys


def graphviz_drawer(distance_matrix, flow_matrix, max_chromosome):
    max_distance = np.max(distance_matrix)
    min_distance = np.min(distance_matrix[np.nonzero(distance_matrix)])
    max_flow = np.max(flow_matrix)
    min_flow = np.min(flow_matrix)

    dot = graphviz.Graph(engine='circo')
    for i in max_chromosome:
        dot.node(str(i - 1), shape='circle')
    for x in range(len(flow_matrix)):
        for y in range(x, len(max_chromosome)):
            flow_value = flow_matrix[max_chromosome[x] - 1, max_chromosome[y] - 1]
            distance_value = distance_matrix[x, y]
            if flow_value != 0:
                flow_value = ((flow_value - min_flow) / (max_flow - min_flow)) * 9 + 1
                dot.edge(str(x), str(y), color=__convert_to_rgb(min_distance, max_distance, distance_value), penwidth=str(flow_value))
    return dot


def __convert_to_rgb(minval, maxval, val):
    colors = [(0, 0, 255), (255, 0, 0)]
    fi = float(val - minval) / float(maxval - minval) * (len(colors) - 1)
    i = int(fi)
    f = fi - i
    if f < sys.float_info.epsilon:
        rgb = colors[i]
    else:
        (r1, g1, b1), (r2, g2, b2) = colors[i], colors[i + 1]
        rgb = int(r1 + f * (r2 - r1)), int(g1 + f * (g2 - g1)), int(b1 + f * (b2 - b1))
    return '#%02x%02x%02x' % rgb

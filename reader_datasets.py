import numpy as np
import json
from urllib import request


def download_datasets_to_file(links_path='datasets_links.json'):
    f = open(links_path)
    data = json.load(f)

    result = []
    for link in data:
        solution = request.urlopen(link['link'])
        solution = solution.read().split(b'\n')
        n = int(solution[0])
        score = int(link['score'])
        distance_matrix = []
        flow_matrix = []
        i = 0
        for line in solution[1:]:
            if not line:
                continue
            if i < n:
                distance_matrix.append([int(x) for x in line.split()])
            else:
                flow_matrix.append([int(x) for x in line.split()])
            i += 1
        result.append(dict(n=n, score=score, distance_matrix=distance_matrix, flow_matrix=flow_matrix))

    with open('datasets.json', 'w') as outfile:
        json.dump(result, outfile)
    

def get_all_datasets_from_file(datasets_path='datasets.json'):
    f = open(datasets_path)
    data = json.load(f)
    for solution in data:
        solution['distance_matrix'] = np.array(solution['distance_matrix'])
        solution['flow_matrix'] = np.array(solution['flow_matrix'])
    return data

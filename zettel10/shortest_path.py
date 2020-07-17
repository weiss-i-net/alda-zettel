import json
import math
import heapq
EARTH_RADIUS = 6378.137

def read_json_to_dict(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def create_graph(distance_dict):
    names = [ name for name in distance_dict ]
    graph = [ [] for _ in names ]
    weights = dict()

    for node in range(len(names)):
        for neighbour_name, distance in distance_dict[names[node]]['Nachbarn'].items():
            neighbour = names.index(neighbour_name)
            graph[node].append(neighbour)
            weights[node, neighbour] = distance
            # weights isnt nessearly symetrical as the steet-lanes could seperate over short
            # distances and have diffrent lenghts (e.g. A8 Albaufstieg)

    return graph, names, weights

def dijkstra(graph, weights, start, destination):
    parent = [ None ] * len(graph)
    q = []
    heapq.heappush(q, (0.0, start, start))

    while q:
        length, node, prev = heapq.heappop(q)
        if parent[node] is None:
            parent[node] = prev
            if node == destination:
                break
            for neighbour in graph[node]:
                if parent[neighbour] is None:
                    neighbour_length = length + weights[(node, neighbour)]
                    heapq.heappush(q, (neighbour_length, neighbour, node))

    path = [ destination ]
    while path[-1] != start:
        path.append(parent[path[-1]])

    return path[::-1], length

def compute_air_distances(distance_dict):
    names = [ name for name in distance_dict ]
    air_distance = dict()

    def translate_coords_to_rad(name):
        north = tuple(map(float, distance_dict[name]['Koordinaten']['Breite'].split('N')))
        east = tuple(map(float, distance_dict[name]['Koordinaten']['Länge'].split('E')))
        return ((north[0] + (north[1] / 60)) / 180 * math.pi,
               (east[0] + (east[1] / 60)) / 180 * math.pi)

    for node_1 in range(len(names)):
        for node_2 in range(len(names)):
            if node_1 != node_2:
                north_1, east_1 = translate_coords_to_rad(names[node_1])
                north_2, east_2 = translate_coords_to_rad(names[node_2])
                air_distance[(node_1, node_2)] = EARTH_RADIUS * math.acos(
                                                 math.sin(north_1)*math.sin(north_2)
                                                 + math.cos(north_1)*math.cos(north_2)*math.cos(east_2-east_1) )

    return air_distance

def a_star(graph, weights, air_distance, start, destination):
    parent = [ None ] * len(graph)
    q = []
    heapq.heappush(q, (0.0, start, start))

    while q:
        length, node, prev = heapq.heappop(q)
        if parent[node] is None:
            parent[node] = prev
            if node == destination:
                break
            for neighbour in graph[node]:
                if parent[neighbour] is None:
                    neighbour_length = length + weights[(node, neighbour)] + air_distance[(node, neighbour)]
                    heapq.heappush(q, (neighbour_length, neighbour, node))

    path = [ destination ]
    while path[-1] != start:
        path.append(parent[path[-1]])

    return path[::-1], length

def print_route_dijkstra(name_start, name_destination, graph, names, weights):
    path, total_distance = dijkstra(graph, weights, names.index(name_start), names.index(name_destination))

    out_string = ''
    for i in range(len(path) - 1):
        out_string += names[path[i]] + '  ==' + str(weights[(path[i], path[i+1])]) + '==>  '
    out_string += name_destination + '  (total: ' + str(total_distance) + ')' + '\n'
    print(out_string)

def print_route_a_star(name_start, name_destination, graph, names, weights, air_distance):
    path, total_distance = a_star(graph, weights, air_distance, names.index(name_start), names.index(name_destination))

    out_string = ''
    for i in range(len(path) - 1):
        out_string += names[path[i]] + '  ==' + str(weights[(path[i], path[i+1])]) + '==>  '
    out_string += name_destination + '  (total: ' + str(total_distance) + ')' + '\n'
    print(out_string)

def main():
    distance_dict = read_json_to_dict('entfernungen.json')
    graph, names, weights = create_graph(distance_dict)


    print_route_dijkstra('Aachen', 'Passau', graph, names, weights)
    print_route_dijkstra('Saarbrücken', 'Leipzig', graph, names, weights)
    print_route_dijkstra('München', 'Greifswald', graph, names, weights)
    print_route_dijkstra('Konstanz', 'Kassel', graph, names, weights)


    air_distance = compute_air_distances(distance_dict)

    print_route_a_star('München', 'Greifswald', graph, names, weights, air_distance)
    print(air_distance[(names.index('Stuttgart'), names.index('München'))])

if __name__ == '__main__':
    main()

def test_air_distance_lt_street_distance():
    distance_dict = read_json_to_dict('entfernungen.json')
    graph, names, weights = create_graph(distance_dict)
    air_distance = compute_air_distances(distance_dict)

    for node_1, node_2 in weights:
        assert weights[node_1, node_2] >= air_distance[node_1, node_2]

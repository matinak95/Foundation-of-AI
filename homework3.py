import sys


def split(self):
    return self.split(' ')


def search_same_page(home, dest, method):
    g = Graph()
    distance = {}
    final_path = []

    g.add_vertex(Vertex(home[0], home[1], home[2]))
    g.add_vertex(Vertex(dest[0], dest[1], dest[2]))

    key1 = (home[0], home[1], home[2])
    key2 = (dest[0], dest[1], dest[2])

    g.add_edge(key1, key2)

    if method == 'BFS':
        distance[key1, key2] = max(abs(key1[2] - key2[2]), abs(key1[1] - key2[1]))
        distance[key2, key1] = max(abs(key1[2] - key2[2]), abs(key1[1] - key2[1]))
    else:
        distance[key1, key2] = max(abs(key1[2] - key2[2]), abs(key1[1] - key2[1])) * 10 \
                               + min(abs(key1[2] - key2[2]), abs(key1[1] - key2[1])) * 4
        distance[key2, key1] = distance[key1, key2]
    [path, cost] = call_search(g, home, dest, distance)
    final_path.append(path[0])

    for gap in range(0, len(path) - 1):
        if path[gap][0] == path[gap + 1][0]:
            x = min(abs(path[gap][1] - path[gap + 1][1]), abs(path[gap][2] - path[gap + 1][2]))
            step = 0
            while x > 0:
                step = step + 1
                final_path.append([path[gap][0], path[gap][1]
                                   + step * (path[gap + 1][1] - path[gap][1]) // (
                                       abs(path[gap][1] - path[gap + 1][1])), path[gap][2]
                                   + step * (path[gap + 1][2] - path[gap][2]) // (
                                       abs(path[gap][2] - path[gap + 1][2]))])
                x = x - 1
            y = max(abs(path[gap][1] - path[gap + 1][1]), abs(path[gap][2] - path[gap + 1][2])) \
                - min((abs(path[gap][1] - path[gap + 1][1]), abs(path[gap][2] - path[gap + 1][2])))
            while y > 0:
                step = step + 1
                if abs(path[gap][1] - path[gap + 1][1]) > abs(path[gap][2] - path[gap + 1][2]):
                    final_path.append([path[gap][0], path[gap][1] + step * (path[gap + 1][1] - path[gap][1])
                                       // (abs(path[gap][1] - path[gap + 1][1])), path[gap + 1][2]])
                else:
                    final_path.append([path[gap][0], path[gap + 1][1], path[gap][2] + step
                                       * (path[gap + 1][2] - path[gap][2]) // (
                                           abs(path[gap][2] - path[gap + 1][2]))])
                y = y - 1

        else:
            final_path.append(path[gap + 1])

    output = open("output.txt", "w+")
    output.write(str(cost) + "\n")
    output.write(str(len(final_path)))

    for i in range(0, len(final_path)):
        output.write("\n")
        if i == 0:
            bid = 0
        elif method == 'BFS':
            bid = 1
        elif final_path[i][0] != final_path[i - 1][0]:
            bid = abs(final_path[i][0] - final_path[i - 1][0])

        elif final_path[i][2] == final_path[i - 1][2] or final_path[i][1] == final_path[i - 1][1]:
            bid = 10
        else:
            bid = 14

        output.write(str(final_path[i][0]) + " " + str(final_path[i][1]) + " "
                     + str(final_path[i][2]) + " " + str(bid))
    sys.exit(0)


def heuristic_finder(v, dest):
    x = abs(dest[0] - v[0]) + max(abs(v[1] - dest[1]), abs(v[2] - dest[2])) * 10 \
                               + min(abs(v[1] - dest[1]), abs(v[2] - dest[2])) * 4
    return x


def remove_vertex_adv(dic, home, dest):
    closed = {}
    hold1 = dic[dest]
    hold2 = dic[home]
    dic[dest] = []
    opened1 = [home]
    closed1 = {home: True}
    while len(opened1) != 0:
        current = opened1.pop(0)
        current_neighbor = dic[current]
        for i in current_neighbor:
            try:
                check = closed1[i]
            except KeyError:
                opened1.append(i)
                closed1[i] = True
    dic[dest] = hold1
    dic[home] = []
    opened2 = [dest]
    closed2 = {dest: True}

    try:
        closed1[dest]
    except KeyError:
        output = open("output.txt", "w+")
        output.write("FAIL")
        sys.exit(0)

    while len(opened2) != 0:
        current = opened2.pop(0)
        current_neighbor = dic[current]
        for i in current_neighbor:
            try:
                check = closed2[i]
            except KeyError:
                opened2.append(i)
                closed2[i] = True
    dic[home] = hold2
    for i in closed1:
        try:
            check = closed2[i]
            closed[i] = closed1[i]
        except KeyError:
            continue

    return closed


class FileReader:
    def __init__(self, file):
        self.file = file
        self.lines = self.file.read().splitlines()
        self.method = self.lines[0]
        self.portal_number = int(self.lines[4])
        self.dimension = list(map(int, self.lines[1].split(' ')))
        self.home = list(map(int, self.lines[2].split(' ')))
        self.destination = list(map(int, self.lines[3].split(' ')))
        self.portals = list(map(split, self.lines[5:5 + self.portal_number]))


def call_search(graph, home, destination, distance):
    minimum_distance = {}
    predecessor = {}
    unfinished = list(graph.vertices.keys())
    inf = 922337203685477500
    final_path = []
    fail = False

    for vertex in unfinished:
        minimum_distance[vertex] = inf

    minimum_distance[(home[0], home[1], home[2])] = 0

    while unfinished:
        min_vertex = None
        for vertex in unfinished:
            if min_vertex is None:
                min_vertex = vertex
            elif minimum_distance[vertex] < minimum_distance[min_vertex]:
                min_vertex = vertex

        for neighbor in graph.vertices[min_vertex].neighbors:
            if distance[min_vertex, neighbor] + minimum_distance[min_vertex] < minimum_distance[neighbor]:
                minimum_distance[neighbor] = distance[min_vertex, neighbor] + minimum_distance[min_vertex]
                predecessor[neighbor] = min_vertex
        if destination == [min_vertex[0], min_vertex[1], min_vertex[2]]:
            break
        unfinished.remove(min_vertex)

    v = destination

    while v != (home[0], home[1], home[2]):
        try:
            final_path.insert(0, list(v))
            v = predecessor[v[0], v[1], v[2]]

        except KeyError:
            fail = True
            output = open("output.txt", "w+")
            output.write("FAIL")
            sys.exit(0)

    final_path.insert(0, home)

    if not fail:
        return final_path, minimum_distance[(destination[0], destination[1], destination[2])]


def start(self):
    return self[0]


def end(self):
    return self[3]


def x_finder(self):
    return self[1]


def y_finder(self):
    return self[2]


def add_neighbor(self, v):
    if v not in self.neighbors:
        self.neighbors.append(v)


class Portals:
    def __init__(self, portals):
        self.portals = portals
        self.portal_start = list(map(start, self.portals))
        self.portal_start_int = list(map(int, self.portal_start))
        self.portal_end = list(map(end, self.portals))
        self.portal_end_int = list(map(int, self.portal_end))
        self.portal_x = list(map(int, list(map(x_finder, self.portals))))
        self.portal_y = list(map(int, list(map(y_finder, self.portals))))
        self.dic = {}

        for ps in range(0, len(self.portal_start_int)):
            try:
                self.dic[self.portal_start_int[ps]].add(self.portal_end_int[ps])
            except KeyError:
                self.dic[self.portal_start_int[ps]] = {self.portal_end_int[ps]}
            # except AttributeError:
            #     self.dic[self.portal_start_int[ps]] = {self.dic[self.portal_start_int[ps]], self.portal_end_int[ps]}
            try:
                self.dic[self.portal_end_int[ps]].add(self.portal_start_int[ps])
            except KeyError:
                self.dic[self.portal_end_int[ps]] = {self.portal_start_int[ps]}
            # except AttributeError:
            #     self.dic[self.portal_end_int[ps]] = {self.dic[self.portal_end_int[ps]], self.portal_start_int[ps]}


class Vertex:

    def __init__(self, year, x, y):
        self.year = year
        self.x_loc = x
        self.y_loc = y
        self.neighbors = []

    def add_neighbor(self, v):
        # if v not in self.neighbors:
        self.neighbors.append(v)


class Graph:
    vertices = {}
    nodes = {}

    def add_vertex(self, vertex):
        # if vertex.year in valid and (vertex.year, vertex.x_loc, vertex.y_loc) not in self.vertices:
        self.vertices[(vertex.year, vertex.x_loc, vertex.y_loc)] = vertex

    def add_edge(self, u, v):
        # if u in self.vertices and v in self.vertices:
        self.vertices[u].add_neighbor(v)
        self.vertices[v].add_neighbor(u)
    #     return True
    # else:
    #     return False


def main():

    file = open("input.txt")

    f = FileReader(file)

    distance = {}
    same_year = {}

    final_path = []

    if f.home == f.destination:
        output = open("output.txt", "w+")
        output.write("0\n1\n" + str(f.home[0]) + " " + str(f.home[1]) + " " + str(f.home[2]) + " " + "0")
        sys.exit(0)

    if f.home[0] == f.destination[0]:
        search_same_page(f.home, f.destination, f.method)

    p = Portals(f.portals)

    try:
        check = p.dic[f.destination[0]]
    except KeyError:
        output = open("output.txt", "w+")
        output.write("FAIL")
        sys.exit(0)
    try:
        check = p.dic[f.home[0]]
    except KeyError:
        output = open("output.txt", "w+")
        output.write("FAIL")
        sys.exit(0)

    keys = list(p.dic.keys())

    for key in keys:
        if len(p.dic[key]) == 1 and key != f.home[0] and key != f.destination[0]:
            try:
                x = p.dic[key].pop()
                p.dic[x].remove(key)
            except KeyError:
                None
            del p.dic[key]

    valid = remove_vertex_adv(p.dic, f.home[0], f.destination[0])

    g = Graph()

    g.add_vertex(Vertex(f.home[0], f.home[1], f.home[2]))
    g.add_vertex(Vertex(f.destination[0], f.destination[1], f.destination[2]))

    same_year[f.home[0]] = [(f.home[0], f.home[1], f.home[2])]
    try:
        same_year[f.destination[0]].append((f.destination[0], f.destination[1], f.destination[2]))
    except KeyError:
        same_year[f.destination[0]] = [(f.destination[0], f.destination[1], f.destination[2])]

    for i in range(0, f.portal_number):
        try:
            check = valid[p.portal_start_int[i]]
            check = valid[p.portal_end_int[i]]
            g.add_vertex(Vertex(p.portal_start_int[i], p.portal_x[i], p.portal_y[i]))
            g.add_vertex(Vertex(p.portal_end_int[i], p.portal_x[i], p.portal_y[i]))
            g.add_edge((p.portal_start_int[i], p.portal_x[i], p.portal_y[i]),
                       (p.portal_end_int[i], p.portal_x[i], p.portal_y[i]))
            try:
                same_year[p.portal_start_int[i]].append((p.portal_start_int[i], p.portal_x[i], p.portal_y[i]))
            except KeyError:
                same_year[p.portal_start_int[i]] = [(p.portal_start_int[i], p.portal_x[i], p.portal_y[i])]
            try:
                same_year[p.portal_end_int[i]].append((p.portal_end_int[i], p.portal_x[i], p.portal_y[i]))
            except KeyError:
                same_year[p.portal_end_int[i]] = [(p.portal_end_int[i], p.portal_x[i], p.portal_y[i])]

            if f.method == 'BFS':
                distance[(p.portal_start_int[i], p.portal_x[i], p.portal_y[i]),
                         (p.portal_end_int[i], p.portal_x[i], p.portal_y[i])] = 1
                distance[(p.portal_end_int[i], p.portal_x[i], p.portal_y[i]),
                         (p.portal_start_int[i], p.portal_x[i], p.portal_y[i])] = 1
            else:
                distance[(p.portal_start_int[i], p.portal_x[i], p.portal_y[i]),
                         (p.portal_end_int[i], p.portal_x[i], p.portal_y[i])] = abs(p.portal_start_int[i]
                                                                                    - p.portal_end_int[i])
                distance[(p.portal_end_int[i], p.portal_x[i], p.portal_y[i]),
                         (p.portal_start_int[i], p.portal_x[i], p.portal_y[i])] = abs(p.portal_start_int[i]
                                                                                      - p.portal_end_int[i])

        except KeyError:
            continue

    if f.method == 'BFS':
        keys1 = list(g.vertices.keys())

        for key in same_year:
            while same_year[key]:
                key1 = same_year[key].pop()
                for key2 in same_year[key]:
                    g.add_edge(key1, key2)
                    distance[key1, key2] = max(abs(key1[2] - key2[2]), abs(key1[1] - key2[1]))
                    distance[key2, key1] = max(abs(key1[2] - key2[2]), abs(key1[1] - key2[1]))

        #
        # while keys1:
        #     key1 = keys1.pop()
        #     for key2 in keys1:
        #         if key1[0] == key2[0]:
        #             g.add_edge(key1, key2)
        #             distance[key1, key2] = max(abs(key1[2] - key2[2]), abs(key1[1] - key2[1]))
        #             distance[key2, key1] = max(abs(key1[2] - key2[2]), abs(key1[1] - key2[1]))

    else:

        if f.method == 'A*':
            heur = heuristic_finder(f.home, f.destination)
            heur = [heur]
            heur.pop()
        for key in same_year:
            while same_year[key]:
                key1 = same_year[key].pop()
                for key2 in same_year[key]:
                    g.add_edge(key1, key2)
                    distance[key1, key2] = max(abs(key1[2] - key2[2]), abs(key1[1] - key2[1])) * 10 \
                                           + min(abs(key1[2] - key2[2]), abs(key1[1] - key2[1])) * 4
                    distance[key2, key1] = distance[key1, key2]

        # keys1 = list(g.vertices.keys())
        # while keys1:
        #     key1 = keys1.pop()
        #     for key2 in keys1:
        #         if key1[0] == key2[0]:
        #             g.add_edge(key1, key2)
        #             distance[key1, key2] = max(abs(key1[2] - key2[2]), abs(key1[1] - key2[1])) * 10 \
        #                                    + min(abs(key1[2] - key2[2]), abs(key1[1] - key2[1])) * 4
        #             distance[key2, key1] = distance[key1, key2]

    [path, cost] = call_search(g, f.home, f.destination, distance)
    final_path.append(path[0])

    for gap in range(0, len(path) - 1):
        if path[gap][0] == path[gap + 1][0]:
            x = min(abs(path[gap][1] - path[gap + 1][1]), abs(path[gap][2] - path[gap + 1][2]))
            step = 0
            while x > 0:
                step = step + 1
                final_path.append([path[gap][0], path[gap][1]
                                   + step * (path[gap + 1][1] - path[gap][1]) // (
                                       abs(path[gap][1] - path[gap + 1][1])), path[gap][2]
                                   + step * (path[gap + 1][2] - path[gap][2]) // (
                                       abs(path[gap][2] - path[gap + 1][2]))])
                x = x - 1
            y = max(abs(path[gap][1] - path[gap + 1][1]), abs(path[gap][2] - path[gap + 1][2])) \
                - min((abs(path[gap][1] - path[gap + 1][1]), abs(path[gap][2] - path[gap + 1][2])))
            while y > 0:
                step = step + 1
                if abs(path[gap][1] - path[gap + 1][1]) > abs(path[gap][2] - path[gap + 1][2]):
                    final_path.append([path[gap][0], path[gap][1] + step * (path[gap + 1][1] - path[gap][1])
                                       // (abs(path[gap][1] - path[gap + 1][1])), path[gap + 1][2]])
                else:
                    final_path.append([path[gap][0], path[gap + 1][1], path[gap][2] + step
                                       * (path[gap + 1][2] - path[gap][2]) // (
                                           abs(path[gap][2] - path[gap + 1][2]))])
                y = y - 1

        else:
            final_path.append(path[gap + 1])

    output = open("output.txt", "w+")
    output.write(str(cost) + "\n")
    output.write(str(len(final_path)))

    for i in range(0, len(final_path)):
        output.write("\n")
        if i == 0:
            bid = 0
        elif f.method == 'BFS':
            bid = 1
        elif final_path[i][0] != final_path[i - 1][0]:
            bid = abs(final_path[i][0] - final_path[i - 1][0])

        elif final_path[i][2] == final_path[i - 1][2] or final_path[i][1] == final_path[i - 1][1]:
            bid = 10
        else:
            bid = 14

        output.write(str(final_path[i][0]) + " " + str(final_path[i][1]) + " "
                     + str(final_path[i][2]) + " " + str(bid))


if __name__ == "__main__":
    main()

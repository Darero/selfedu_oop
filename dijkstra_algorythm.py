import sys


class Descriptor:
    def __set_name__(self, owner, name):
        self.name = '_' + name

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        setattr(instance, self.name, value)


class Vertex:
    links = Descriptor()

    def __init__(self):
        self.links = []


class Link:
    v1 = Descriptor()
    v2 = Descriptor()
    dist = Descriptor()

    def __init__(self, vertex_1, vertex_2, dist=1):
        self.v1 = vertex_1
        self.v2 = vertex_2
        self.dist = dist
        if vertex_2 not in vertex_1.links:
            vertex_1.links.append(vertex_2)
        if vertex_1 not in vertex_2.links:
            vertex_2.links.append(vertex_1)


class LinkedGraph:
    links = Descriptor()
    vertex = Descriptor()

    def __init__(self):
        self.links = []
        self.vertex = []
        self.check_lst = [(link.v1, link.v2) for link in self.links]

    def add_link(self, link):
        self.check_lst = [(link.v1, link.v2) for link in self.links]
        if (link.v1, link.v2) not in self.check_lst and (link.v2, link.v1) not in self.check_lst:
            self.links.append(link)
        if link.v1 not in self.vertex:
            self.vertex.append(link.v1)
        if link.v2 not in self.vertex:
            self.vertex.append(link.v2)

    def add_vertex(self, v):
        if v not in self.vertex:
            self.vertex.append(v)

    def find_path(self, start_v, stop_v):
        return self.dijkstra_algorithm(start_v, stop_v)

    def dijkstra_algorithm(self, start, stop):
        vertexes = self.vertex[:]  # поверхностная копия списка вершин
        shortest_path = dict()
        previous = dict()
        prev_links = dict()
        for vertex in vertexes:
            shortest_path[vertex] = sys.maxsize  # выставляем бесконечное расстояние до вершин, кроме стартовой
        shortest_path[start] = 0
        while vertexes:  # проходим по списку, пока не закончатся вершины
            current_min_vertex = None
            for vertex in vertexes:
                if current_min_vertex is None:
                    current_min_vertex = vertex
                elif shortest_path[vertex] < shortest_path[current_min_vertex]:  # находим текущую наименьшую вершину
                    current_min_vertex = vertex
            neighboors = {i: list(filter(lambda x: x != current_min_vertex, [i.v1, i.v2]))[0]
                          for i in self.links if
                          current_min_vertex in (i.v1, i.v2)}  # словарь вида соединение: вершина (сосед)
            for neighboor in neighboors:
                distance = shortest_path[current_min_vertex] + neighboor.dist  # находим длину до вершины
                if distance < shortest_path[neighboors[neighboor]]:
                    shortest_path[neighboors[
                        neighboor]] = distance  # присваиваем звание короткого пути соседу, если текущий меньше предыдущего
                    previous[neighboors[neighboor]] = current_min_vertex
                    prev_links[neighboors[neighboor]] = neighboor
            vertexes.remove(current_min_vertex)  # убираем из списка наименьшую вершину
        path_v = []
        path_l = []
        vertex = stop

        while vertex != start:
            path_v.append(vertex)
            path_l.append(prev_links[vertex])
            vertex = previous[vertex]
        path_v.append(start)
        return list(reversed(path_v)), list(reversed(path_l))


class Station(Vertex):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class LinkMetro(Link):
    def __init__(self, v1, v2, dist):
        super().__init__(v1, v2, dist)


map_metro = LinkedGraph()
v1 = Station("Сретенский бульвар")
v2 = Station("Тургеневская")
v3 = Station("Чистые пруды")
v4 = Station("Лубянка")
v5 = Station("Кузнецкий мост")
v6 = Station("Китай-город 1")
v7 = Station("Китай-город 2")

map_metro.add_link(LinkMetro(v1, v2, 1))
map_metro.add_link(LinkMetro(v2, v3, 1))
map_metro.add_link(LinkMetro(v1, v3, 1))

map_metro.add_link(LinkMetro(v4, v5, 1))
map_metro.add_link(LinkMetro(v6, v7, 1))

map_metro.add_link(LinkMetro(v2, v7, 5))
map_metro.add_link(LinkMetro(v3, v4, 3))
map_metro.add_link(LinkMetro(v5, v6, 3))

print(len(map_metro._links))
print(len(map_metro._vertex))
path = map_metro.find_path(v1, v6)  # от сретенского бульвара до китай-город 1
print(path[0])  # [Сретенский бульвар, Тургеневская, Китай-город 2, Китай-город 1]
print(sum([x.dist for x in path[1]]))  # 7

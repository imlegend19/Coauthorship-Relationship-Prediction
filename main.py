from __future__ import division
from collections import defaultdict
import xlrd

types = {"Author": 0, "Paper": 1, "Venue": 2}
node_indexes = {}
nodes = set()
node_types = {}


class Node:
    def __init__(self, value, tpe, index):
        self.type = tpe
        self.value = value
        self.index = index


class Graph:

    def __init__(self):
        self.graph = defaultdict(list)

    def add_edge(self, node1, node2):
        self.graph[node1.index].append(node2.index)
        self.graph[node2.index].append(node1.index)

    def bfs(self, s):
        visited = [False] * (len(self.graph))

        meta_path = [0, 1, 2, 1, 0]
        index = 1

        queue = [s]

        visited[s] = True
        m = self.graph[s]

        paths = []

        for i in m:
            if node_types[i] == meta_path[index] and not visited[i]:
                queue.append(i)
                visited[i] = True
                n = self.graph[i]
                for j in n:
                    if node_types[j] == meta_path[index + 1] and not visited[j]:
                        queue.append(j)
                        b = self.graph[j]
                        for k in b:
                            if node_types[k] == meta_path[index + 2] and not visited[k]:
                                queue.append(k)
                                visited[k] = True
                                v = self.graph[k]
                                for l in v:
                                    if node_types[l] == meta_path[index + 3] and not visited[l]:
                                        queue.append(l)
                                        # print(queue)
                                        paths.append(list(queue))
                                        queue.pop()
                                    if v.index(l) == len(v) - 1:
                                        visited[queue.pop()] = False
                            if b.index(k) == len(b) - 1:
                                visited[queue.pop()] = False
                    if n.index(j) == len(n) - 1:
                        visited[queue.pop()] = False
            if m.index(i) == len(m) - 1:
                visited[m.pop()] = False

        return paths


graph = Graph()


def build_graph():
    wb = xlrd.open_workbook('data.xlsx')
    sheet = wb.sheet_by_index(0)

    num_rows = sheet.nrows
    num_cells = sheet.ncols

    lst = []

    for i in range(num_cells):
        lst.append(sheet.cell_value(0, i))

    index = 0
    for i in range(1, num_rows):
        value1 = sheet.cell_value(i, 0)
        type1 = int(sheet.cell_value(i, 1))
        value2 = sheet.cell_value(i, 2)
        type2 = int(sheet.cell_value(i, 3))

        temp = node_indexes.values()

        node1_index = None
        node2_index = None

        if value1 not in temp:
            node_indexes[index] = value1
            node1_index = index
            index += 1
        else:
            for inx, val in node_indexes.items():
                brk = False
                if val == value1:
                    node1_index = inx
                    brk = True

                if brk:
                    break

        if value2 not in temp:
            node_indexes[index] = value2
            node2_index = index
            index += 1
        else:
            for inx, val in node_indexes.items():
                brk = False
                if val == value2:
                    node2_index = inx
                    brk = True

                if brk:
                    break

        node1 = Node(value1, type1, node1_index)
        node2 = Node(value2, type2, node2_index)

        nodes.add(node1)
        nodes.add(node2)

        graph.add_edge(node1=node1, node2=node2)

    print("Graph")
    print("********************************************")
    print(graph.graph)

    print("\n")

    print("Node Indexes allocated")
    print("********************************************")
    print(node_indexes)


def calculate_measures(src_paths, dest_paths, src, dest):
    print("Path Count")
    print("********************************************")
    print("Path count measures the number of path instances between two objects following a given meta path, denoted "
          "as PC - R , where R is the relation denoted by the meta path. Path count can be calculated by the products "
          "of adjacency matrices associated with each relation in the meta path.")

    print("Path Count: %d \n" % len(src_paths))

    print("Normalised Path Count")
    print("********************************************")
    print("Normalized path count is to discount the number of paths between two objects in the network by their "
          "overall connectivity.")

    src_to_dest = []
    for i in src_paths:
        if i[4] == dest:
            src_to_dest.append(list(i))

    dest_to_src = []
    for i in dest_paths:
        if i[4] == src:
            dest_to_src.append(list(i))

    # print(src_to_dest)
    # print(dest_to_src)

    npc = (len(src_to_dest) + len(dest_to_src)) / (len(src_paths) + len(dest_paths))

    print("Normalised Path Count: %.2f \n" % npc)

    print("Random Walk")
    print("********************************************")
    print("Random walk measure along a meta path is defined as RW-R (ai, aj) = PC(ai, aj) / PC(ai, .) which is a "
          "natural generalization of PropFlow")

    rw = len(src_to_dest)/len(src_paths)
    rw_inv = len(dest_to_src)/len(dest_paths)

    print("Random Walk: %.2f \n" % rw)

    print("Symmetric Random Walk")
    print("********************************************")
    print("Symmetric random walk considers the random walk from two directions along the meta path, and defined as "
          "SRW(ai, aj) = RW(ai, aj) + RW-inverse(aj, ai).")

    srw = rw + rw_inv

    print("Symmetric Random Walk: %.2f" % srw)


def run_bfs():
    build_graph()

    for i in nodes:
        node_types[i.index] = int(i.type)

    print("\n")
    print("Node Types with indexes")
    print("********************************************")
    print(node_types)
    print("\n")

    src_paths = graph.bfs(0)
    dest_paths = graph.bfs(14)

    print("Source meta-paths")
    print("********************************************")
    print(src_paths)

    print("\n")

    print("Destination meta-paths")
    print("********************************************")
    print(dest_paths)

    print("\n")

    calculate_measures(src_paths, dest_paths, 0, 14)


if __name__ == '__main__':
    run_bfs()

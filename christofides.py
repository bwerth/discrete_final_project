'''
1. Create MST
2. Get set of odd vertices
3. Find min weight perfect matching (M) from odd vertices
4. Make multigraph from M and MST
5. Find Euler circuit in multigraph
6. Turn Euler circuit into Hamilton circuit
'''
from mst2 import *
from tsp import *
from blossom import *

# import Bryan's min weight perfect match stuff here

def christofides(graph: 'Graph'):
    edges = [(n1.point,n2.point,dist(n1,n2)) for n1,n2 in graph.get_edges()]
        # 'edges' is technically a graph, don't worry
    MST_tree = find_mst2(graph)
    # odd_verts = find_odd_verts(MST_tree)
    # print(MST_tree)
    MST_tree = minimum_weight_match(MST_tree)
    euc = euler_circ(MST_tree, graph)
    # curr = euc[0]
    curr = 0
    path = [curr]
    visited = [False]*len(euc)
    visited[0] = True
    length = 0
    # TODO: so 'i' is a tuple, which obviously you can't index with....
    print(euc)
    euc_temp = euc.copy()
    for i in euc[1:]:
        temp_ind = euc_temp.index(i)
        if not visited[temp_ind]:
            euc_temp[temp_ind] = ' '
            path.append(i)
            visited[temp_ind] = True
            # print(edges[curr][temp_ind])
            # length += edges[curr][2]
            curr = i
    path.append(path[0])
    return path

def find_odd_verts(mst):
    temp = {}
    verts = []
    for edge in mst:
        if edge[0] not in temp:
            temp[edge[0]] = 0
        if edge[1] not in temp:
            temp[edge[1]] = 0
        temp[edge[0]] += 1
        temp[edge[1]] += 1
    for vert in temp:
        if temp[vert] % 2 == 1:
            verts.append(vert)
    return verts

def euler_circ(matched_mst, uhh):
    nabes = {}
    for edge in matched_mst:
        if edge[0] not in nabes:
            nabes[edge[0]] = []
        if edge[1] not in nabes:
            nabes[edge[1]] = []
        nabes[edge[0]].append(edge[1])
        nabes[edge[1]].append(edge[0])
    # SIKE BITCH we're also finding the Hamilton circuit
    start_vert = matched_mst[0][0]
    euc = [nabes[start_vert][0]]
    while len(matched_mst) > 0:
        for i, v in enumerate(euc):
            if len(nabes[v]) > 0:
                break
        while len(nabes[v]) > 0:
            w = nabes[v][0]
            edge_remove(matched_mst, v, w)
            del nabes[v][(nabes[v].index(w))]
            del nabes[w][(nabes[w].index(v))]
            i = i+1
            euc.insert(i,w)
            v = w
    # print(type(euc))
    return euc

def edge_remove(matched_mst, v1, v2):
    for i, item in enumerate(matched_mst):
        if (item[0]==v2 and item[1]==v1) or (item[0]==v1 and item[1]==v2):
            del matched_mst[i]
    return matched_mst


if __name__ == '__main__':
    # d = [
    #     [(0, 0), (1, 1)],  # simple two-point line
    #     [(0, 0), (0, 1), (1, 2), (2, 3), (0, 0)],  # a cycle
    #     [(1, 2), (4, 5), (2, 3)],  # a bent three-point line
    # ]
    d = [[(1380, 939), (2848, 96), (3510, 1671), (457, 334), (3888, 666),
        (984, 965), (2721, 1482), (1286, 525), (2716, 1432), (738, 1325),
        (1251, 1832), (2728, 1698), (3815, 169), (3683, 1533), (1247, 1945)]]
        # (123, 862), (1234, 1946), (252, 1240), (611, 673), (2576, 1676),
        # (928, 1700), (53, 857), (1807, 1711), (274, 1420), (2574, 946),
        # (178, 24), (2678, 1825), (1795, 962), (3384, 1498), (3520, 1079),
        # (1256, 61), (1424, 1728), (3913, 192), (3085, 1528), (2573, 1969),
        # (463, 1670), (3875, 598), (298, 1513), (3479, 821), (2542, 236),
        # (3955, 1743), (1323, 280), (3447, 1830), (2936, 337), (1621, 1830),
        # (3373, 1646), (1393, 1368), (3874, 1318), (938, 955), (3022, 474),
        # (2482, 1183), (3854, 923), (376, 825), (2519, 135), (2945, 1622),
        # (953, 268), (2628, 1479), (2097, 981), (890, 1846), (2139, 1806),
        # (2421, 1007), (2290, 1810), (1115, 1052), (2588, 302), (327, 265),
        # (241, 341), (1917, 687), (2991, 792), (2573, 599), (19, 674),
        # (3911, 1673), (872, 1559), (2863, 558), (929, 1766), (839, 620),
        # (3893, 102), (2178, 1619), (3822, 899), (378, 1048), (1178, 100),
        # (2599, 901), (3416, 143), (2961, 1605), (611, 1384), (3113, 885),
        # (2597, 1830), (2586, 1286), (161, 906), (1429, 134), (742, 1025),
        # (1625, 1651), (1187, 706), (1787, 1009), (22, 987), (3640, 43),
        # (3756, 882), (776, 392), (1724, 1642), (198, 1810), (3950, 1558)]
    g = Graph.from_drawing(d)
    path = christofides(g)
    print(path)
    # print(length)

















# oof

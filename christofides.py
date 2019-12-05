'''
1. Create MST
2. Get set of odd vertices
3. Find min weight perfect matching (M) from odd vertices
4. Make multigraph from M and MST
5. Find Euler circuit in multigraph
6. Turn Euler circuit into Hamilton circuit
'''

# import Bryan's min weight perfect match stuff here

def get_odd_verts(mst):
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
    while len(matched_mst) > 0
        for i, v in enumerate(euc):
            if len(nabes[v]) > 0:
                break
        while len(nabes[v]) > 0:
            w = nabes[v][0]
            edge_remove(matched_mst, v, w)
            del nabes[v][(nabes[w].index(v))]
            i = i+1
            euc.insert(i,w)
            v = w
    return euc

def edge_remove(matched_mst, v1, v2):
    for i, item in enumerate(matched_mst):
        if (item[0]==v2 and item[1]==v1) or (item[0]==v1 and item[1]==v2):
            del matched_mst[i]
    return matched_mst




















# oof

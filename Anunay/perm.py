def get_perm(total_vert, edges, community_init):

	comm = [(0,0) for i in range(total_vert)]
	for i in community_init:
		comm[i[0]] = i
	nieghbours = {}

	for i in edges:
	    u = i[0]
	    v = i[1]
	    # print(i)
	    if(u in nieghbours):
	        nieghbours[u].add(v)
	    else:
	        nieghbours[u] = set([v])
	    if(v in nieghbours):
	        nieghbours[v].add(u)
	    else:
	        nieghbours[v] = set([u])

	for i in nieghbours:
	    nieghbours[i] = list(nieghbours[i])
	val = 0
	for i in range(total_vert):
	    k = get_perm_single(total_vert,edges,i,nieghbours[i],comm)
	    # print(i,k)
	    val += k

	val /= total_vert

	return val

def get_perm_single(total_vert, edges, node_v, nieghbours, community_init):
    numerator = 0
    denominator = 0
    Etemp_v = 0

    E_v = [0 for i in range(total_vert + 1)]

    I_v, Emax_v, D_v = 0,0,0
    cin_v = 0
    l = 0
    for i in range(len(nieghbours)):
        l = i
        ng = nieghbours[i]
        if(community_init[ng][1] == community_init[node_v][1]):
            I_v += 1
        else:
            E_v[community_init[ng][1]] += 1
            Etemp_v = E_v[community_init[ng][1]]
            # print(Etemp_v,",",i)
            if(Etemp_v > Emax_v):
                Emax_v = Etemp_v

        if(community_init[ng][1] != community_init[node_v][1]):
            continue;
        for j in range(i + 1,len(nieghbours)):
            ng2 = nieghbours[j]

            if(community_init[ng2][1] != community_init[node_v][1]):
                continue
            denominator += 1

            if((ng,ng2) in edges or (ng2,ng) in edges):
                numerator += 1
#     print(Emax_v)
    if(Emax_v == 0):
        Emax_v = 1
    # print(nieghbours)
    if(len(nieghbours) > 0):
        D_v = len(nieghbours)
    else:
        D_v = 1	

    if(denominator == 0):
        cin_v = 0
    else:
        cin_v = (1.0*numerator)/denominator
    # print(I_v, Emax_v,D_v,cin_v)
    return ((1.0*I_v)/(Emax_v*D_v)) - 1 + cin_v

def hub_node_graph(left_size,right_size):
    edges = []

#     g = Graph()
    total_vert = left_size + right_size + 1
#     g.add_vertices(total_vert)
    
    hub_node = 0
    offset_right = left_size + 1
    
    edges.extend(creat_random_connected(0,left_size + 1))
    edges.extend(creat_random_connected(offset_right,right_size))

    for i in range(right_size):
        edges.append((0,offset_right + i));
#     print(edges)
#     g.add_edges(edges)
    return [total_vert, edges]


n, e = map(int,input().split())
edges = []
for i in range(e):
	r = list(map(int,input().split()))
	edges.append(r)
comm = []
for i in range(n):
	r = tuple(map(int,input().split()))
	comm.append(r)
print(get_perm(n,edges,comm))
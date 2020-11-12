from copy import deepcopy
max_iter = 10
def metric(comm,adj):
	mod = 0
	m = 0
	for i in adj:
		m += len(adj[i])
	for i in comm:
		for a1 in comm[i]:
			for a2 in comm[i]:
				if(a2 in adj[a1] and a1 != a2):
					mod += (1 - len(adj[a1])*len(adj[a2])/m)
	mod /= m
	return mod
def louvain(total_vert,edges):
	k = 0 #iteration
	adj = {}
	for i in edges:
		if(i[0] in adj):
			adj[i[0]].add(i[1])
		else:
			adj[i[0]] = set([i[1]])
		if(i[1] in adj):
			adj[i[1]].add(i[0])
		else:
			adj[i[1]] = set([i[0]])
	comm = {}
	node_comm_mapp = {}
	for i in range(total_vert):
		comm[i] = set([i])
		node_comm_mapp[i] = i
	history = []
	val = metric(comm,adj)
	while True:
		val_old = val
		while True:
			val_new = val_old
			vertex_move = False
			for i in range(total_vert):
				inc = 0
				my_com = node_comm_mapp[i]
				for j in adj[i]:
					comm_copy = deepcopy(comm)
					comm1 = node_comm_mapp[i]
					comm2 = node_comm_mapp[j]
					comm_copy[comm1].discard(i)
					comm[comm2].add(i)
					val_change = metric(comm,adj)
					comm[comm1].add(i)
					comm[comm2].discard(i)
					if((val_change - val_new) > inc):
						inc = val_change - val_new
						my_com = comm2
				comm[node_comm_mapp[i]].discard(i)
				comm[my_com].add(i)
				if(my_com != node_comm_mapp[i]):
					vertex_move = True
				node_comm_mapp[i] = my_com
				val_new += inc;
				print(inc,"inc")
			# print(comm,"changed")
			if(not(vertex_move) or (val_new - val_old) < 0 ):
				break
			else:
				val_old = val_new
		print(adj,"djeiqdhqisn0cnqacs")
		val_changed = metric(comm,adj)
		print(comm,val_changed,adj)
		if((val_changed - val_old) < 0 or k == max_iter):
			break
		val = val_changed
		cnt = 0
		history.append([val,comm,adj])
		mapping = {}
		for i in comm:
			if(len(comm[i]) > 0):
				mapping[i] = cnt
				cnt += 1
		new_adj = {}
		for i in range(cnt):
			new_adj[i] = set([])
		for i in adj:
			for v in adj[i]:
				u = i
				if(node_comm_mapp[u] != node_comm_mapp[v]):
					new_adj[mapping[node_comm_mapp[u]]].add(mapping[node_comm_mapp[v]])
					new_adj[mapping[node_comm_mapp[v]]].add(mapping[node_comm_mapp[u]])
		node_comm_mapp = {}
		comm = {}
		for i in range(cnt):
			node_comm_mapp[i] = i
			comm[i] = set([i])
		total_vert = cnt
		adj = new_adj
		k += 1
		if(cnt == 1):
			break
	for i in history:
		print(i)
	print(history)
	return comm		
print(louvain(5,[(1,2),(2,0),(0,1),(3,1),(4,3)]))
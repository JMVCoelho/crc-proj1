import pandas as pd
import networkx as nx


def process(edges_path: str, name1: str, name2: str):
    # name1 = user, name2 = business

    g = pd.read_csv(edges_path, delim_whitespace=True)

    users = []
    businesses = []

    g['user'] = g['user'].apply(lambda x: 'U_' + str(x))
    g['business'] = g['business'].apply(lambda x: 'B_' + str(x))

    for user in g['user']:
        users.append(user)

    for business in g['business']:
        businesses.append(business)

    users = sorted(list(set(users)))
    businesses = sorted(list(set(businesses)))

    with open(name1 + ".users", 'w') as uf:
        for user in users:
            uf.write(user + " " + "User\n")

    with open(name2 + ".business", 'w') as uf:
        for business in businesses:
            uf.write(business + " " + "Business\n")

    g.to_csv("bipartite-user-business.edges", sep=" ", header=False, index=False)

    return g


def create_projections(bipartite_path: str, nodes_path: str, name: str):
    B = nx.algorithms.bipartite.edgelist.read_edgelist(bipartite_path, nodetype=str, data=(("weight", int),))
    data = pd.read_csv(nodes_path, delim_whitespace=True, names=['nodes', 'types'])
    nodes = data.nodes.to_list()

    projection = nx.bipartite.projected_graph(B, nodes)

    if len(projection) > 0:
        nx.write_edgelist(projection, name + '.edges', data=False)
        print('Wrote', name + '.edges')
        return projection

    return None



#create_projections('bipartite-user-business.edges', 'users-node-list.users', 'user-projection')
#create_projections('bipartite-user-business.edges', 'business-node-list.business', 'business-projection')
exit(0)

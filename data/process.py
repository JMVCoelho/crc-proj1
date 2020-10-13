import pandas as pd

file = "rec-yelp-user-business.edges"
g = pd.read_csv(file, delim_whitespace=True)

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

with open("users-node-list.users", 'w') as uf:
    for user in users:
        uf.write(user + " " + "User\n")

with open("business-node-list.business", 'w') as uf:
    for business in businesses:
        uf.write(business + " " + "Business\n")

g.to_csv("bipartite-user-business.edges", sep=" ", header=False, index=False)



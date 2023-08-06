from math import sqrt

def eigenvector_centrality(G, max_iter=100, tol=1.0e-6, nstart=None,
                           weight='weight'):

    if type(G) == nx.MultiGraph or type(G) == nx.MultiDiGraph:
        raise nx.NetworkXException("Not defined for multigraphs.")
  
    if len(G) == 0:
        raise nx.NetworkXException("Empty graph.")
  
    if nstart is None:
        x = dict([(n,1.0/len(G)) for n in G])
    else:
        x = nstart
  
    s = 1.0/sum(x.values())
    for k in x:
        x[k] *= s
    nnodes = G.number_of_nodes()
    
    for i in range(max_iter):
        xlast = x
        x = dict.fromkeys(xlast, 0)
  
        for n in x:
            for nbr in G[n]:
                x[nbr] += xlast[n] * G[n][nbr].get(weight, 1)
  
        try:
            s = 1.0/sqrt(sum(v**2 for v in x.values()))

        except ZeroDivisionError:
            s = 1.0
        for n in x:
            x[n] *= s

        err = sum([abs(x[n]-xlast[n]) for n in x])
        if err < nnodes * tol:
            return x
  
    raise nx.NetworkXError("""eigenvector_centrality(): power iteration failed to converge in %d iterations."%(i+1))""")
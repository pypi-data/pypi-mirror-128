def betweenness_centrality(G, k=None, normalized=True, weight=None,
                           endpoints=False, seed=None):
  
    betweenness = dict.fromkeys(G, 0.0)  
    if k is None:
        nodes = G
    else:
        random.seed(seed)
        nodes = random.sample(G.nodes(), k)
    for s in nodes:
        if weight is None:
            S, P, sigma = _single_source_shortest_path_basic(G, s)
        else:  
            S, P, sigma = _single_source_dijkstra_path_basic(G, s, weight)
  
        if endpoints:
            betweenness = _accumulate_endpoints(betweenness, S, P, sigma, s)
        else:
            betweenness = _accumulate_basic(betweenness, S, P, sigma, s)

    betweenness = _rescale(betweenness, len(G), normalized=normalized,
                           directed=G.is_directed(), k=k)
    return betweenness
from math import sqrt

def katz_centrality(G, alpha=0.1, beta=1.0, max_iter=1000, tol=1.0e-6, nstart=None, normalized=True, weight = 'weight'):
  
  if len(G) == 0:
    return {}
    
  nnodes = G.number_of_nodes()
  
  if nstart is None:
    x = dict([(n,0) for n in G])
  else:
    x = nstart
  
  try:
    b = dict.fromkeys(G,float(beta))
  except (TypeError,ValueError,AttributeError):
    b = beta
    if set(beta) != set(G):
      raise nx.NetworkXError('beta dictionary '
                                   'must have a value for every node')
  

    for i in range(max_iter):
      xlast = x
      x = dict.fromkeys(xlast, 0)
  
      for n in x:
        for nbr in G[n]:
          x[nbr] += xlast[n] * G[n][nbr].get(weight, 1)
      for n in x:
        x[n] = alpha*x[n] + b[n]
  
        
      err = sum([abs(x[n]-xlast[n]) for n in x])
      if err < nnodes*tol:
        if normalized:
          try:
            s = 1.0/sqrt(sum(v**2 for v in x.values()))
          except ZeroDivisionError:
            s = 1.0
        else:
          s = 1
        for n in x:
          x[n] *= s
        return x
  
  raise nx.NetworkXError('Power iteration failed to converge in''%d iterations.' % max_iter)
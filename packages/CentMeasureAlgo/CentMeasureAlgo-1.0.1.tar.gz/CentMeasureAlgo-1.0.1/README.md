# CentMeasureAlgo
Package for 15XW98 
 A personal package to help with the various centrality measure algorithims available. Currently contains:
 * Betweenes Measure 
 * Closeness Measure
 * Eigenvector
 * Katz's Measure

Ongoing project. (Current date Nov 2021)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install CentMeasureAlgo
```

## Documentation for CentMeasureAlgo

<details>
    <summary>Betweenes Measure</summary>   
    
    Parameters
    ----------
    G : graph
      A NetworkX graph.
  
    k : int, optional (default=None)
      If k is not None use k node samples to estimate betweenness.
      The value of k <= n where n is the number of nodes in the graph.
      Higher values give better approximation.
  
    normalized : bool, optional
      If True the betweenness values are normalized by `2/((n-1)(n-2))`
      for graphs, and `1/((n-1)(n-2))` for directed graphs where `n`
      is the number of nodes in G.
  
    weight : None or string, optional (default=None)
      If None, all edge weights are considered equal.
      Otherwise holds the name of the edge attribute used as weight.
  
    endpoints : bool, optional
      If True include the endpoints in the shortest path counts.
  
    Returns
    -------
    nodes : dictionary
       Dictionary of nodes with betweenness centrality as the value.
  
</details>

___

<details>
    <summary>Closeness Measure</summary>
  
    Parameters
    ----------
    G : graph
      A NetworkX graph
    u : node, optional
      Return only the value for node u
    distance : edge attribute key, optional (default=None)
      Use the specified edge attribute as the edge distance in shortest 
      path calculations
    normalized : bool, optional
      If True (default) normalize by the number of nodes in the connected
      part of the graph.
  
    Returns
    -------
    nodes : dictionary
      Dictionary of nodes with closeness centrality as the value.
  
</details>

___

<details>
    <summary>Eigenvector</summary>

    Parameters
    ----------
    G : graph
      A networkx graph
  
    max_iter : integer, optional
      Maximum number of iterations in power method.
  
    tol : float, optional
      Error tolerance used to check convergence in power method iteration.
  
    nstart : dictionary, optional
      Starting value of eigenvector iteration for each node.
  
    weight : None or string, optional
      If None, all edge weights are considered equal.
      Otherwise holds the name of the edge attribute used as weight.
  
    Returns
    -------
    nodes : dictionary
       Dictionary of nodes with eigenvector centrality as the value.
  
</details>
  
___

<details>
    <summary>Katz Measure</summary>
  
    Parameters
    ----------
    G : graph
      A NetworkX graph
  
    alpha : float
      Attenuation factor
  
    beta : scalar or dictionary, optional (default=1.0)
      Weight attributed to the immediate neighborhood. 
      If not a scalar, the dictionary must have an value
      for every node.
  
    max_iter : integer, optional (default=1000)
      Maximum number of iterations in power method.
  
    tol : float, optional (default=1.0e-6)
      Error tolerance used to check convergence in
      power method iteration.
  
    nstart : dictionary, optional
      Starting value of Katz iteration for each node.
  
    normalized : bool, optional (default=True)
      If True normalize the resulting values.
  
    weight : None or string, optional
      If None, all edge weights are considered equal.
      Otherwise holds the name of the edge attribute
      used as weight.
  
    Returns
    -------
    nodes : dictionary
       Dictionary of nodes with Katz centrality as 
       the value.
  
    Raises
    ------
    NetworkXError
       If the parameter `beta` is not a scalar but 
       lacks a value for at least  one node
 
</details>

 
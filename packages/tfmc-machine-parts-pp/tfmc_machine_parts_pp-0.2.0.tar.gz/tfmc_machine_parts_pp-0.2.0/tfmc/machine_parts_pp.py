# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Copyright 2021 TechnipFMC
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

"""
This module provides an API for accessing the machine parts data and dissimilarities.
In particular, the API offers functionality for generation of clustering problems of 
ordered data in terms of planted partitions.

For a description of the data, please see <LINK TO DATA ARTICLE>.

"""


__version__ = '0.2.0'

def get_parts_csv_file_name():
    '''
    Returns the absolute path to the csv file containing the machine parts
    and the part of relations.
    '''
    return _get_local_fname('parts.csv')

def get_dissimilarities_csv_file_name():
    '''
    Returns the absolute path to the csv file containing the machine part
    dissimilarities.
    '''
    return _get_local_fname('dissimilarities.csv')

def get_all_machine_parts():
    '''
    Returns all machine parts in a dict with items on the form

    (parent_id, (child_id_1,...,child_id_n)).

    That is, for every vertex id, the dict maps to the list of child vertices.
    All identifiers are integers.
    '''
    ccs  = get_machine_part_connected_components()
    full = dict(ccs[0])
    for cc in ccs[1:]:
        full.update(cc)
        
    return full

def get_all_dissimilarities():
    '''
    Returns a symmetric numpy array dissimilarity coefficients between machine parts.
    All dissimilarities are in the range [0,1].
    '''
    import numpy as np
    fname = _get_local_fname('dissimilarities.csv')
    N     = len(get_all_machine_parts())
    dists = np.zeros((N,N), dtype=float)
    with open(fname, 'r') as inf:
        for line in inf.readlines():
            a,b,d = line.split(',')
            a,b,d = [int(a),int(b),float(d)]
            dists[a,b] = d
            dists[b,a] = d

    return dists

def get_machine_part_connected_components(spec=None):
    '''
    Returns all machine parts in a list of dicts, wher ach dict has items on the form

    (parent_id, (child_id_1,...,child_id_n)).

    That is, for every vertex id, the dict maps to the list of child vertices.
    All identifiers are integers.

    Each dict constitutes a connected component of machine parts, and the union of the
    dicts is equivalent to the graph returned by get_all_machine_parts().

    If no spec is given, then all connected components are returned.
    If spec is an iterable of integers in the range {0,..,7}, then the specified
    connected components are returned.
    If spec is an integer in the range {0,..,7}, then this particular connected component 
    is returned.
    '''
    import json
    with open(_get_local_fname('machine_parts.json'), 'r') as inf:
        data = json.load(inf)

    ccs = [_complete_dict(_int_dict(cc)) for cc in data['ccs']]

    if spec is None:
        return ccs

    try:
        return [ccs[i] for i in spec]
    except TypeError as e:
        # Not iterable --- hoping for an integer.
        return ccs[spec]

def planted_partition(base,n,mu,var):
    '''
    Generates a planted partition based on the cc spec with multiplicity n+1.

    base - base graph to multiplicate, obtained from 
           get_machine_part_connected_components(...) or random_induced_subgraph(...)
    n    - number of copies to make
    var  - variance of the applied dissimilarity noise

    Returns X,D,PP where
    X  - a dict-graph of all the vertices
    D  - A numpy dissimilarity array
    PP - A list of lists, each list a collection of copy-equivalent elements
    '''
    C0         = _complete_dict(base)
    X,D        = _gen_rebased_dissim_space(C0)
    XX,DD,PP,_ = _gen_planted_partition(X,D,n,mu,var)
    return XX,DD,PP

class MinDegNotSatisfiableError(Exception):
    '''
    Exception thrown by random_induced_subgraph if the minimum degree
    requirement cannot be satisfied.
    '''
    def __init__(self,minDeg):
        self.minDeg = minDeg
        Exception.__init__(self,'minDeg >= %1.3f impossible.' % minDeg)

        
def random_induced_subgraph(ccs,m,minDeg=0):
    '''
    Produces a graph by making a draw of m random vertices from ccs, 
    and generating the induced subgraph based on the transitive closure of ccs.
    If minDeg is specified, successive draws will be done until the average in/out
    degree of the induced subgraph is minDeg. If no such graph is found after
    1000 attempts, the method exits with a 
    fmcti.machine_parts_pp.MinDegNotSatisfiableError

    ccs    - the graph to sample from
    m      - the size of the induced subgraph vertex set
    minDeg - minimal acceptable in-out degree

    Returns a graph of m vertices of minimum in/out degree minDeg.
    '''
    import numpy as np

    ccs = _transitive_closure(ccs)
    res = _draw_subgraph(ccs,m)
    cnt = 1
    while np.mean([len(res[x]) for x in res]) < minDeg:
        if cnt >= 1000:
            raise MinDegNotSatisfiableError(minDeg)

        cnt += 1
        res  = _draw_subgraph(ccs,m)

    return res

def clustering_to_cluster_index_mapping(clusters):
    '''
    Produces a mapping from all indices in the base space
    to the cluster index of the clusters.

    clusters - list of clusters
    
    Returns a dict with elements ( x , index of cluster containing x )
    '''
    mapping = {}
    for clstId in range(len(clusters)):
        for x in clusters[clstId]:
            mapping[x] = clstId

    return mapping
            
def _draw_subgraph(ccs,m):
    '''
    Generates a random induced subgraph of ccs of m vertices.
    ccs - complete graph
    m   - size of induced subgraph
    '''
    import numpy as np
    import numpy.random as npr

    assert len(ccs) >= m
    ids = npr.permutation(list(ccs))[:m] 
    return {i:[x for x in ccs[i] if x in ids] for i in ids}

def _transitive_closure(graph):
    '''
    Modifies the passed graph by adding relations to achieve
    the transitive closure of graph.
    graph - The dict graph to compyte the transitive closure of
    Returns the passed graph object
    '''
    visited = set()
    X       = list(graph)
    for x in graph:
        graph[x] = _descendants_of(graph,x,X,visited)

    return graph

def _descendants_of(graph, x, X, visited):
    '''
    Part of the _transitive_closure method.
    '''
    if x in visited:
        return graph[x]

    visited.add(x)

    all_decs = set(graph[x])
    for y in list(graph[x]):
        decs = _descendants_of(graph,y,X,visited)
        all_decs.update(decs)

    graph[x] = sorted(all_decs)
        
    return graph[x]
        
def _int_dict(parts):
    '''
    Returns a dict with keys converted to ints.
    '''
    return {int(x):parts[x] for x in parts}

def _complete_dict(parts):
    '''
    Ensures that the key set matches the full set of vertices in the graph.
    Note: the function modifies the passed dict.
    '''
    # Only need to possibly add child identifieres
    ids = set.union(*[set(y) for _,y in parts.items()])
    for i in ids:
        if not i in parts:
            parts[i] = []

    return parts

def _get_local_fname(short_name):
    '''
    Produces an installation independent path to the file short_name, assuming the
    file is containeed in this module.
    '''
    import os.path 
    import sys
    module_filename = sys.modules[__name__].__file__
    module_dirname  = os.path.dirname(module_filename)
    return os.path.join(module_dirname, short_name)


def _gen_rebased_dissim_space(parts):
    '''
    Based on the passed parts, the method rebases the part indices and produces
    a dissimilarity matrix with corresponding dissimilarities.
    Returns (parts,dissim-matrix)
    '''
    import numpy as np
    rename,inv_rename = _rebase_map(parts)
    dissims = get_all_dissimilarities()
    N       = len(parts)

    res_parts = {rename(x) : [rename(y) for y in parts[x]] for x in parts}
    res_diss  = np.zeros((N,N), dtype=float)
    for i in np.arange(N):
        ii = inv_rename(i)
        for j in np.arange(i+1,N):
            jj = inv_rename(j)
            res_diss[i,j] = dissims[ii,jj]
            res_diss[j,i] = dissims[jj,ii]

    return (res_parts, res_diss)


def _rebase_map(parts):
    '''
    Use this method to obtain a renaming of party types identifiers so that
    they make up a contigous sequence of integers starting at 0.

    Note that the rename function is determinied stocahstically, so the 
    _rebase_map function is not deterministic.

    parts - one single dict of parts

    Returns two functions (rename,inv_rename) that map int -> int.
    rename is the rename function, and inv_rename is the inverse of rename.
    '''
    import numpy.random as npr
    
    ids        = list(npr.permutation(list(parts)))
    rename     = lambda x : ids.index(x)
    inv_rename = lambda y : ids[y]

    return (rename,inv_rename)
    
def _gen_planted_partition(parts,dissims,M,mu,var,no_rename=False):
    '''
    Generates a planted partition over the indices in parts by
    providing M additional copies of parts.

    parts   - rebased part set
    dissims - rebased dissimilarities
    M       - the required number of additional copies of parts
    mu      - the mean of the Gaussian noise added to dissimilarities
    var     - the variance of the Gaussian noise added to dissimilarities

    no_rename - If True, then the planted partitions will be on the form
                [0,n,2n],[1,n+1,2n+1],... where n is the number of elements
                in parts. This is mainly for testing and debugging purposes.

    Returns (all_parts, all_dissims,PP,(rename, inv_name)) 
    where all_parts is a dict defining all elements and relations in the 
    proliferated dataset,
    all_dissims specifies all dissimilarities, PP is the list of
    planted partitions (that is, a list of lists, where each nested list
    is a set of copy-paste vertex ids), and (rename,inv_name) are the rename 
    and inverse rename fuctions used to re-label the vertices.
    
    Notices that the returned problem set is (stochastically) re-based prior to 
    returning, to avoid trivial correlation rules for the elements in the planted 
    partition.
    '''
    import numpy as np

    n = len(parts)
    N = n*(M+1)

    new_parts = dict(parts)
    for i in range(M):
        offset       = (i+1)*n
        offset_parts = {(x+offset):[y+offset for y in parts[x]] for x in parts}
        new_parts.update(offset_parts)

    assert len(new_parts) == N

    # We construct the dissimilarities block-wise.
    # Diagonal blocks are dissims, and off-diagonal
    # blocks are perturbed dissims. Remember that the blocks array
    # must be transpose-symmetric (symmetric elements must be the transpose
    # of each other)
    blocks = [[None]*(M+1) for _ in np.arange(M+1)]
    for i in np.arange(M+1):
        blocks[i][i] = dissims
        for j in np.arange(i+1,M+1):
            blocks[i][j] = _perturbe(dissims,mu,var)
            blocks[j][i] = blocks[i][j].T
            
    new_dissims = np.block(blocks)
    
    # Planted partitions are now sequential
    PP = [np.arange(i, n*(M+1), n) for i in np.arange(n)]
        
    # Sanity check...
    assert np.sum([len(p) for p in PP]) == N

    # And now rebase all to re-name vertices
    rename,inv_name = _rebase_map(new_parts)
    if no_rename:
        rename   = lambda x : x
        inv_name = rename

    ren_parts   = {rename(x):[rename(y) for y in new_parts[x]] for x in new_parts}
    ren_dissims = np.zeros_like(new_dissims)
    for i in np.arange(N):
        for j in np.arange(i+1,N):
            ren_dissims[i,j] = new_dissims[inv_name(i),inv_name(j)]
            ren_dissims[j,i] = ren_dissims[i,j]

    ren_pp = [[rename(x) for x in p] for p in PP]

    return ren_parts, ren_dissims, ren_pp, (rename, inv_name)
    
    
def _perturbe(dists,mu,var):
    '''
    Perturbes the dissimilarities with Gaussian noise with variance var,
    using rejection sampling until all pertrubed values are in the range [0,1].
    '''
    import numpy as np
    from numpy.random import normal as N
    assert np.all((0 <= dists) & (dists <= 1))
    result = np.array(dists, dtype=float)
    ok     = np.full(dists.shape, False, dtype=bool)
    while not np.all(ok):
        result[~ok] = dists[~ok] + N(mu,var,size=np.sum(~ok))
        ok = (0.0 <= result) & (result <= 1.0)

    return result

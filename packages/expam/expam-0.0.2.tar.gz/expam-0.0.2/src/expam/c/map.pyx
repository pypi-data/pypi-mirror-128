#cython: infer_types=True
#cython: boundscheck=False
#cython: wraparound=False
#cython: nonecheck=False
#cython: cdivision=True

cimport cython
from libc.math cimport floor
import numpy as np
cimport numpy as np

ctypedef np.uint16_t uint16_t
ctypedef np.uint64_t uint64_t

cpdef binarysearch(uint64_t[:] target, uint64_t[:, :] kmers):
    """Binary search for target within array of kmers. Will return closest
    element in list if target is not found.

    :param target: Element to search for.
    :param kmers: Array to be searched within.s
    :return: Whether element was found, and the corresponding index.
    :rtype: (int, int)

    """
    cdef:
        long long int i=0
        long long int L=0, U=kmers.shape[0]-1
        int j=0, W=kmers.shape[1]

    while True:
        if L > U:
            # Return the index with a fail signal.
            return 0, i
        i = <long long int>floor((U + L) / 2)
        for j in range(W):
            if kmers[i, j] > target[j]:
                U = i - 1
                break
            elif kmers[i, j] < target[j]:
                L = i + 1
                break
        else:
            return 1, i

def binarysearch_put(uint64_t[:, :] kmers, uint64_t[:, :] keys, uint16_t[:] values, uint16_t[:, :] lca_matrix, int new_id):
    """For all the elements in kmers, each coming from a node in the phylogeny
    with ID new_id, update their LCA values to incorporate this new_id. All
    possible LCA values have been computed in the LCA matrix.

    This means that every value in kmers should be in keys, as a binary search
    is executed to find the value of each kmer in keys.

    :param kmers: New items to be mapped.
    :param keys: (Sorted) Database keys to be searched against.
    :param values: Current LCA values for keys.
    :param lca_matrix: LCAs for each pair of nodes in the phylogeny.
    :param int new_id: ID of node containing kmers.
    :return: None (in-place)

    """
    cdef:
        long long int i, ind, M=kmers.shape[0]
        bint isin
        uint16_t current_id

    for i in range(M):
        # Find value in list.
        isin, ind = binarysearch(
            kmers[i, :],
            keys
        )

        # Find LCA of new and current value.
        current_id = values[ind]
        if current_id == new_id:
            pass
        elif current_id == 0:
            values[ind] = new_id
        elif current_id < new_id:
            values[ind] = lca_matrix[new_id, current_id]
        elif current_id > new_id:
            values[ind] = lca_matrix[current_id, new_id]

cpdef binarysearch_get(uint64_t[:, :] kmers, uint64_t[:, :] keys, uint16_t[:] values, uint16_t nullvalue):
    """Get the value of each element in kmers from keys. If the element is not
    found, nullvalue is used instead.

    :param kmers: Array of kmers to be searched for in keys.
    :param keys: Sorted database keys.
    :param values: Corresponding LCA values for keys.
    :param nullvalue: Value to be used if searched item is not found.
    :return: Array of values.
    :rtype: np.ndarray

    """
    cdef:
        long long int i, j, ind
        bint isin
        long long int M=kmers.shape[0]

    results = np.empty(M, dtype=np.uint16)
    cdef uint16_t[:] results_view = results
    for i in range(M):
        isin, ind = binarysearch(
            kmers[i, :],
            keys
        )
        if isin == 0:
            results_view[i] = nullvalue
        else:
            results_view[i] = values[ind]
    return results

cdef common_clade(uint16_t[:] nodes, uint16_t[:, :] lca_matrix, uint16_t null_value):
    """
    Class codes:
        0   -->     classified
        1   -->     split
        -1  -->     unclassified

    """

    cdef:
        int cls
        uint16_t lca, t_lca
        int l
        int i, j

    cls = 0

    l = nodes.shape[0]
    j = 0

    # Remove unknown kmers.
    for i in range(l):
        if nodes[i] == null_value:
            cls = 1

        else:
            nodes[j] = nodes[i]
            j += 1

    if j == 0:
        return -1, null_value

    nodes = nodes[:j]

    lca = nodes[0]

    for i in range(j):

        # lca_matrix is lower triangular, so catch the edge case where
        # the [i,i] value in the matrix is 0, but they obviously are
        # compatible.
        if nodes[i] == lca:
            continue

        if lca > nodes[i]:
            t_lca = lca_matrix[lca, nodes[i]]
        else:
            t_lca = lca_matrix[nodes[i], lca]

        # If we have found a split, we can't push lower than the
        # split point.
        if cls == 1:
            if t_lca != lca and t_lca != nodes[i]:
                lca = t_lca

        else:
            # Otherwise continue to push as low as possible.
            if t_lca == lca:
                lca = nodes[i]

            elif t_lca == nodes[i]:
                pass

            else:
                cls = 1
                lca = t_lca

    return cls, lca

cpdef classify(int k, uint64_t[:, :] kmers, uint64_t[:, :] keys, uint16_t[:] values,
               uint16_t[:, :] lca_matrix, uint16_t null_value):
    """
    Classification algorithm.

    """

    cdef:
        uint16_t[:] maps
        int cls
        uint16_t lca

    maps = binarysearch_get(kmers[:, 1:], keys, values, null_value)
    cls, lca = common_clade(maps, lca_matrix, null_value)

    return cls, lca, maps

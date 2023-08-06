#cython: infer_types=True
#cython: boundscheck=False
#cython: wraparound=False
#cython: nonecheck=False
#cython: cdivision=True

cimport cython
from libc.math cimport ceil, floor
import numpy as np
cimport numpy as np

ctypedef np.uint16_t uint16_t
ctypedef np.uint64_t uint64_t

cpdef binarysearch(uint64_t[:] target, uint64_t[:, :] kmers):
    """Binary search for target within array of kmers. Will return closest
    element in list if target is not found.

    :param target: Element to search for.
    :param kmers: Array to be searched within.
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

cpdef classify(uint64_t[:, :] kmers, uint64_t[:, :] keys, uint16_t[:] values,
               uint16_t[:, :] lca_matrix, uint16_t null_value, float alpha=1.0):
    cdef:
        uint16_t[:] comp_nodes, comp_counts
        uint16_t[:] raw_mapped_kmers
        int cls, n_candidates, cls_code = 0         # Innocent until proven guilty for class code.
        int required_counts
        str comp_string

    # Map kmers using database.
    raw_mapped_kmers = binarysearch_get(kmers[:, 1:], keys, values, null_value)

    # Convert mapped read to compressed string format.
    comp_nodes, comp_counts = kmers_to_compressed_form(raw_mapped_kmers, keys, values, null_value)
    comp_string = compressed_to_string(comp_nodes, comp_counts)

    # Catch case of all unclassified.
    if comp_nodes.shape[0] == 1 and comp_nodes[0] == null_value:
        return -1, null_value, comp_string

    # Classification from lineage(s), with cutoff from alpha.
    required_counts = ceil(alpha * kmers.shape[0])
    nodes, counts = np.unique(raw_mapped_kmers, return_counts=True)     # Returns in sorted order.

    # Ignore unclassified counts.
    if nodes[0] == null_value:      # Null value is smaller than any nodes.
        nodes = nodes[1:]
        counts = counts[1:]

        cls_code = 1

    # Get list of lowest points satisfying cutoff criterion.
    candidate_nodes, candidate_counts, n_candidates = accumulate_candidates(nodes, counts, lca_matrix, required_counts)

    if n_candidates == 0:
        cls_code, cls = -1, null_value
    else:
        cls = choose_candidate(candidate_nodes[:n_candidates], candidate_counts[:n_candidates], lca_matrix)

        if n_candidates > 1:
            cls_code = 1

    return cls_code, cls, comp_string

cdef kmers_to_compressed_form(uint16_t[:] raw_mapped_kmers, uint64_t[:, :] keys, uint16_t[:] values, uint16_t null_value):
    """
    Return two arrays:
        1. Array of phylogeny nodes that consecutive kmers mapped to.
        2. The number of consecutive kmers that mapped to this node.

    """
    cdef:
        uint16_t[:] nodes, counts
        int n_kmers, required_counts
        int i, j = 0

    # Compress to consecutive appearances.
    n_kmers = raw_mapped_kmers.shape[0]
    nodes = np.ndarray(n_kmers, dtype=np.uint16)
    counts = np.ones(n_kmers, dtype=np.uint16)
    
    nodes[0] = raw_mapped_kmers[0]

    for i in range(1, n_kmers):
        if raw_mapped_kmers[i] == nodes[j]:
            counts[j] += 1
        else:
            j += 1
            nodes[j] = raw_mapped_kmers[i]

    return nodes[:j], counts[:j]

cdef str compressed_to_string(uint16_t[:] nodes, uint16_t[:] counts):
    cdef:
        int i, n_chunks = nodes.shape[0]
        str output = ""

    for i in range(n_chunks):
        output += "p%d:%d " % (nodes[i], counts[i])

    return output

cdef accumulate_candidates(uint16_t[:] nodes, uint16_t[:] counts, uint16_t[:, :] lca_matrix, int required_counts):
    cdef:
        int i, j, n_nodes = nodes.shape[0], n_candidates = 0
        uint16_t[:] candidate_nodes, candidate_counts
        uint8_t[:] candidacy_status
        uint16_t lca

    candidacy_status = np.zeros(n_nodes, dtype=np.uint8)            # 0 :: unchecked, +1 :: been checked.
    candidate_nodes = np.ndarray(n_nodes, dtype=np.uint16)
    candidate_counts = np.ndarray(n_nodes, dtype=np.uint16)

    for i in range(n_nodes - 1, 0, -1):
        if candidacy_status[i] == 0:        # i.e. a child has not been made candidate.
            if counts[i] >= required_counts:
                n_candidates = add_candidate(nodes[i], counts[i], candidate_nodes, candidate_counts, n_candidates)
                candidacy_status[i] = 1     # This node is now a candidate.

            for j in range(i - 1, -1, -1):
                lca = lca_matrix[nodes[i], nodes[j]]

                if lca == nodes[j]:
                    counts[j] += counts[i]
                    candidacy_status[j] = candidacy_status[i]

                    break

    return candidate_nodes, candidate_counts, n_candidates

cdef int add_candidate(uint16_t node, uint16_t counts, uint16_t[:] candidate_nodes, uint16_t[:] candidate_counts, int j):
    candidate_nodes[j] = node
    candidate_counts[j] = counts

    return j + 1

cdef uint16_t choose_candidate(uint16_t[:] candidate_nodes, uint16_t[:] candidate_counts, uint16_t[:, :] lca_matrix):
    cdef:
        uint16_t cls, counts
        int i, n_candidates = candidate_nodes.shape[0]

    cls = candidate_nodes[0]
    counts = candidate_counts[0]

    for i in range(1, n_candidates):
        if candidate_counts[i] > counts:
            cls = candidate_nodes[i]
            counts = candidate_counts[i]

        elif candidate_counts[i] == counts:
            cls = lca_matrix[cls, candidate_nodes[i]]

    return cls


"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        DEPRECATED
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


"""

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


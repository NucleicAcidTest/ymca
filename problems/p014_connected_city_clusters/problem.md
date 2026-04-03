# P014 Connected City Clusters

## Summary

Cities are connected by bidirectional roads, and the road network is given as a `0/1` matrix.

Determine how many internally connected city clusters exist in the network.

Print the total number of connected clusters.

## Matching Hints

- The statement talks about a state with city clusters connected by roads.
- Roads are bidirectional and there are no connections between different clusters.
- Input is an adjacency matrix where entry `(i, j)` is `1` if city `i` is connected to city `j`.
- Output asks for the total number of connected clusters.

## Notes

- This is the number of connected components in an undirected graph.
- The screenshot shows an input header like `matInput_row matInput_col`, followed by the matrix rows.
- In practice the matrix is square, so the archived solution uses the row count `N` as the number of cities and reads the first `N` values from each row.
- The example matrix in the screenshot has three connected components, so the output is `3`.

# Graph Analysis for CARP Instances

## Project Description
A Python implementation for analyzing mixed graphs (with both directed and undirected edges) with support for:
- Graph metrics calculation (density, degrees, shortest paths)
- Floyd-Warshall algorithm for shortest paths
- Betweenness centrality calculation
- Reading CARP (Capacitated arc routing problem) instance files (.dat format)

## Features

### Graph Metrics Calculated

1. **Number of vertices**  
   Total count of nodes in the graph

2. **Number of edges**  
   Total count of undirected connections

3. **Number of arcs**  
   Total count of directed connections

4. **Number of required vertices**  
   Nodes that must be visited/serviced

5. **Number of required edges**  
   Undirected connections that must be traversed

6. **Number of required arcs**  
   Directed connections that must be traversed

7. **Graph density (order strength)**  
   Ratio of existing connections to possible connections  
   `Density = (|E| + |A|) / (|V| * (|V| - 1))`

8. **Minimum vertex degree**  
   Smallest number of connections to any node

9. **Maximum vertex degree**  
    Largest number of connections to any node

10. **Betweenness centrality**  
    Measures how often a node appears on shortest paths between other nodes  
    *(Alternative paths not calculated)*

11. **Average path length**  
    Mean distance between all vertex pairs

12. **Graph diameter**  
    Longest shortest path in the graph

### Implemented Algorithms
- Floyd-Warshall for shortest paths
- Betweenness centrality calculation

## Project Structure

- /projeto_carp_grafos
- README.md
- grafo.py 

- /selected_instances/.dat files

## Basic Usage

- g = ler_arquivo_dat('selected_instances/###.dat') - Load instance
- g.show_stats()  -  Displays statistics
- g.show_betweenness()  - Shows centrality

  
## Credits
- Lucca Guedes Batistela
- Prof. Mayron César O. Moreira
- UFLA


## Authors
- Lucca Guedes Batistela - 202320985
- Carlos Eduardo Borges de Sousa - 202020296

## Course Information
- Course: GCC218 - Algoritmos em Grafos
- Professor: Mayron César de Oliveira Moreira

# Graph Analysis and Visualization for CARP Instances

## Overview
This project implements a comprehensive solution for analyzing and visualizing CARP (Capacitated Arc Routing Problem) instances. It provides tools for graph analysis, solution construction using greedy algorithms, and visualization of results.

## Project Structure
```
projeto_carp_grafos/
├── src/
│   ├── grafo.py                 # Core graph implementation
│   ├── grafo_add.py            # Graph addition operations
│   ├── grafo_analise.py        # Graph analysis functions
│   ├── grafo_visualizacao.py   # Graph visualization utilities
│   ├── greedy_constructor.py   # Greedy algorithm implementation
│   ├── main.py                 # Main execution file
│   ├── solucao_writer.py       # Solution output handling
│   ├── utils_grafo.py          # Utility functions
│   ├── comparar_resultados.py  # Results comparison tool
│   └── visualizacao_resultados.ipynb  # Jupyter notebook for visualization
├── selected_instances/         # CARP instance files
├── padroes/                    # Pattern files
└── requirements.txt           # Project dependencies
```

## Features

### 1. Graph Analysis
- Total number of vertices, edges, and arcs.
- Number of required vertices, edges, and arcs.
- Graph density, minimum and maximum vertex degrees.
- Average path length and graph diameter.
- Betweenness centrality (intermediation) for each vertex.

### 2. Solution Construction
- Greedy algorithm implementation for CARP
- Solution optimization
- Multiple solution strategies

### 3. Visualization
- Interactive graph visualization
- Metrics and statistics display
- Solution path visualization
- Comparative analysis tools

### 4. Data Processing
- CARP instance parsing
- Solution validation
- Results comparison
- Output generation

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd projeto_carp_grafos
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Main Program
```bash
python src/main.py [instance_file]
```

### Using the Visualization Notebook
1. Launch Jupyter Notebook:
```bash
jupyter notebook
```

2. Open `src/visualizacao_resultados.ipynb`

3. Configure the instance file path:
```python
arquivo = "path/to/your/instance.dat"
```

4. Run all cells to generate visualizations

### Comparing Results
```bash
python src/comparar_resultados.py [solution1] [solution2]
```

## Dependencies
- Python 3.x
- matplotlib==3.10.3
- numpy==2.2.6
- pandas==2.2.3
- networkx==3.2.1
- seaborn==0.13.2
- jupyter==1.0.0
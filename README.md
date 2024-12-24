# Graph-neural-network-for-IIT

# Dataset and Program Description

Due to the file size, the dataset can be downloaded from [Zenodo](https://zenodo.org/records/14551717). 

## Folder Structure and Data Contents

### 1. `random_graph_data_non_extrapolative_setting` and `random_graph_data_extrapolative_setting`
- These folders, located in the same directory as the Jupyter Notebook files, contain the graph data used for the first and second experiments, respectively.
- Each folder includes subdirectories (`N=*_meta`) organized by the value of \(N\), storing the following meta-information for each system:
  - Node connections
  - Edge values
  - Node states
  - The value of \(T\)
- Each folder also contains `summary_N=*.csv` files summarizing the corresponding data.

### 2. `random_graph_data_N=100`
- This folder contains the graph data used in experiments with \(N=100\).
- Files are organized by the value of \(p_e\), with each pickle file including 100 test systems:
  - The first 50 systems are entirely dense graphs, where each pair of nodes is connected with a probability of 0.4. These systems are not described in the paper.
  - The second 50 systems are the split-brain-like systems analyzed in the paper.
- Excel files in this folder are included for reference only.

### 3. `prelearned_model`
- This folder contains 100 pre-trained GNN models, trained during the first experiment using the proposed method
- Input statistics (mean and standard deviation) are also provided.

## Workflow for `random_graph_data_non_extrapolative_setting` and `random_graph_data_extrapolative_setting`
1. **Execute `graph_neural_network_for_IIT.ipynb`:**
   - The program reads and processes summary files and meta-information.
     
## Workflow for `random_graph_data_N=100`
1. **Execute `graph_neural_network_for_IIT.ipynb`:**
   - The program utilizes both the pickle files from `random_graph_data_N=100` and the pre-trained models from `prelearned_model` for processing.
2. **Summarize results:**
   - After executing the first step, use `bigN_result_processing.ipynb` to summarize the output results.

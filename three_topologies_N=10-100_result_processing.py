import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.ticker import FormatStrFormatter

# =======================
# Setting
# =======================
target_dir = 'result/'  # specify the name of the result_folder generated automatically when executing the graph_nueral_network_for_IIT.ipynb
n_values = list(range(10, 101, 10))    
categories = ['Tree', 'Full', 'Random' ]
colors = {'Tree': 'blue', 'Random': 'green', 'Full': 'red'}
offsets = {'Tree': 0.0, 'Random': 0.0, 'Full': 0.9}   
category_rows = {'Tree': range(0, 10), 'Random': range(10, 20), 'Full': range(20, 30)} 
phi_colname = 'EstimatePhi'


# labels in the legend
category_labels = {
    'Tree': 'Tree-like',
    'Random': 'Loop-containing',
    'Full': 'Fully connected',
}




# =======================
# dictionary for data storage
# =======================
phi_per_network = {cat: {} for cat in categories}
phi_per_category_avg = {cat: {} for cat in categories}


# =======================
# Read data and calculate averages
# =======================
for N in n_values:
    pattern = os.path.join(target_dir, f'*_N={N}.xlsx')
    file_list = sorted(glob.glob(pattern))
    if len(file_list) != 100:
        print(f"Warning: The number of files regarding N={N} is {len(file_list)} not 100. Please check. Now, skip this N")
        continue

    phi_matrix = []
    for file in file_list:
        df = pd.read_excel(file)
        phi_matrix.append(df[phi_colname].values)
    phi_matrix = np.array(phi_matrix)  # shape: (100, 30)

    for cat in categories:
        row_indices = category_rows[cat]

        phi_avg = np.mean(phi_matrix[:, row_indices], axis=0)
        phi_per_network[cat][N] = phi_avg  



# =======================
# graph 1 big_phi 
# =======================
plt.figure(figsize=(10, 6))
ax = plt.gca()

for cat in categories:
    xs = []
    ys = []
    for N in n_values:
        if N in phi_per_network[cat]:
            for val in phi_per_network[cat][N]:
                xs.append(N + offsets[cat])
                ys.append(val)
    plt.scatter(xs, ys, color=colors[cat], label=category_labels[cat], alpha=0.7)
plt.xlabel('$N$', fontsize=16)
plt.ylabel('Estimated integrated information', fontsize=16)

plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.ylim(bottom=0)

ax.set_xticks(list(range(10, 101, 10)))
ax.grid(True, axis='x', which='major', color='black', alpha=0.3)  
ax.grid(True, axis='y', which='major', color='black')       



plt.legend(fontsize=15, facecolor='white', edgecolor='black', framealpha=1)
plt.tight_layout()
plt.savefig('big_phi.png')
plt.close()



# =======================
# Major Complex Size based on the estimated label
# =======================

label_threshold = 0.6  # threshold


mc_per_network = {cat: {} for cat in categories}

for N in n_values:
    pattern = os.path.join(target_dir, f'*_N={N}.xlsx')
    file_list = sorted(glob.glob(pattern))
    if len(file_list) != 100:
        continue

    label_tensor = np.zeros((100, 30, N)) 
    for file_idx, file in enumerate(file_list):
        df = pd.read_excel(file)
        for row_idx in range(30):
            label_vec = eval(df.loc[row_idx, 'Est_label'])
            label_tensor[file_idx, row_idx, :] = np.array(label_vec)

    for cat in categories:
        row_indices = category_rows[cat]
        mc_list = []
        for r in row_indices:
            avg_vec = np.mean(label_tensor[:, r, :], axis=0)
            major_count = np.sum(avg_vec >= label_threshold)
            mc_ratio = major_count / N
            mc_list.append(mc_ratio)
        mc_per_network[cat][N] = mc_list 




# =======================
# graph 2  Major Complex Ratio
# =======================
offsets = {'Tree': 0.0, 'Random': -1.0, 'Full': 1.5}

plt.figure(figsize=(10, 6))
ax = plt.gca()

spread = 0.9  
bin_decimals = 6

for cat in categories:
    xs = []
    ys = []
    for N in n_values:
        if N not in mc_per_network[cat]:
            continue

        x_center = N + offsets[cat] 

        groups = {}
        for v in mc_per_network[cat][N]: 
            key = round(float(v), bin_decimals) if bin_decimals > 0 else float(v)
            groups.setdefault(key, []).append(v)

        for key, group_vals in groups.items():
            m = len(group_vals)
            if m == 1:
                xs.append(x_center)
                ys.append(group_vals[0])
            else:
                offsets_local = np.linspace(-spread, spread, m)
                xs.extend(x_center + offsets_local)
                ys.extend([group_vals[0]] * m)

    if xs:
        plt.scatter(xs, ys, color=colors[cat], label=category_labels[cat], alpha=0.7)

plt.xlabel('$N$', fontsize=16)
plt.ylabel('Ratio of nodes in the major complex', fontsize=16)

ax.set_xticks(list(range(10, 101, 10)))
ax.grid(True, axis='x', which='major', color='black', alpha=0.3)  
ax.grid(True, axis='y', which='major', color='black')       

ax.yaxis.set_major_formatter(FormatStrFormatter('%g'))

plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.ylim(bottom=0)
plt.legend(fontsize=15, facecolor='white', edgecolor='black', framealpha=1)
plt.tight_layout()
plt.savefig('major_complex_ratio.png')
plt.close()


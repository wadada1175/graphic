import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np
import math

# ネットワークデータを読み込む
edges = []
with open('network_data.txt', 'r') as f:
    for line in f:
        node1, node2 = map(int, line.split())
        edges.append((node1, node2))

# クラスタデータを読み込む
clusters = {}
with open('cluster_data.txt', 'r') as f:
    for line in f:
        node, cluster = map(int, line.split())
        clusters[node] = cluster

# ネットワークグラフを作成
G = nx.Graph()
G.add_edges_from(edges)

# クラスタごとのノードを色分けするためのカラーマップを生成
unique_clusters = set(clusters.values())
cluster_colors = {
    cluster: "#" + ''.join([random.choice('0123456789ABCDEF') for _ in range(6)])
    for cluster in unique_clusters
}

# ノードの色リストを作成
node_colors = [cluster_colors[clusters[node]] for node in G.nodes()]

# クラスタごとのノードリストを作成
cluster_nodes = {
    cluster: [node for node, cl in clusters.items() if cl == cluster]
    for cluster in unique_clusters
}

# レイアウトの初期化
pos = {}
cluster_count = len(unique_clusters)

# グリッドサイズを決定
cols = math.ceil(math.sqrt(cluster_count))
rows = math.ceil(cluster_count / cols)

cluster_idx = 0
cluster_offset = {}
grid_spacing = 15  # クラスタ間の距離を調整

for cluster in unique_clusters:
    row = cluster_idx // cols
    col = cluster_idx % cols
    # クラスタのオフセットを計算
    offset = np.array([col * grid_spacing, row * grid_spacing])
    cluster_offset[cluster] = offset
    cluster_idx += 1

# 各クラスタのノード位置を計算
for cluster, nodes in cluster_nodes.items():
    # クラスタ内のレイアウト
    subgraph = G.subgraph(nodes)
    # ノード間の距離を調整するために 'k' と 'scale' を設定
    sub_pos = nx.spring_layout(subgraph, k=1.5, scale=5)
    # オフセットを適用して位置を調整
    offset = cluster_offset[cluster]
    for node in sub_pos:
        pos[node] = sub_pos[node] + offset

# ネットワークグラフを描画
plt.figure(figsize=(12, 12))
nx.draw(
    G, pos, with_labels=True, node_size=500, node_color=node_colors,
    font_size=10, font_weight='bold', edge_color='gray'
)
plt.title('BA Model Network with Clustering')
plt.show()
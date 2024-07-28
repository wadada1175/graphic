import networkx as nx
import matplotlib.pyplot as plt
import random

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
cluster_colors = {cluster: "#" + ''.join([random.choice('0123456789ABCDEF') for _ in range(6)]) for cluster in unique_clusters}

# ノードの色リストを作成
node_colors = [cluster_colors[clusters[node]] for node in G.nodes()]

# ネットワークグラフを描画
plt.figure(figsize=(12, 12))
nx.draw(G, with_labels=True, node_size=500, node_color=node_colors, font_size=10, font_weight='bold', edge_color='gray')
plt.title('BA Model Network with Clustering')
plt.show()
import matplotlib.pyplot as plt
import numpy as np
import umap as um
from tqdm import tqdm
from customEmbeddings import MyCustomEmbedding

def project_embeddings(embeddings, umap_transform, batch_size):
    umap_embeddings = np.empty((len(embeddings),2))
    batch = np.empty((batch_size))
    for cycle in tqdm(range(0, len(embeddings), batch_size)):
        batch = embeddings[cycle:cycle+batch_size]
        umap_embeddings[cycle:cycle+batch_size] = umap_transform.transform(batch)
    return umap_embeddings

def visualise_embeddings(query, results, full_embeddings, expanded_embeddings=None):
    embedding_function = MyCustomEmbedding()
    _visualise_embeddings(embedding_function(query), results, full_embeddings, expanded_embeddings)

def _visualise_embeddings(query_embeddings, results_embeddings, full_embeddings, expanded_embeddings=None):
    batch_size = 32
    umap_transform = um.UMAP().fit(full_embeddings)
    projected_results_embedding = project_embeddings(results_embeddings, umap_transform, batch_size)
    #projected_full_embedding = project_embeddings(full_embeddings, umap_transform, batch_size)
    projected_query_embedding = project_embeddings(query_embeddings, umap_transform, batch_size)
    fig, ax = plt.subplots()
    #ax.scatter(projected_full_embedding[:, 0], projected_full_embedding[:, 1], s=5, label="Full Embeddings", facecolor='yellow', edgecolor='black')
    ax.scatter(projected_query_embedding[:, 0], projected_query_embedding[:, 1], s=70, label="Query Embedding", color='red')
    ax.scatter(projected_results_embedding[:, 0], projected_results_embedding[:, 1], s=70, label="Original Top 5 Result Embeddings", color='blue')
    if(expanded_embeddings!=None):
        projected_expanded_queries = project_embeddings(expanded_embeddings, umap_transform, batch_size)
        ax.scatter(projected_expanded_queries[:,0], projected_expanded_queries[:,1], s=50, label="Results after query expansion", color="green")
    ax.legend()
    ax.grid(True)
    plt.gca().set_aspect('equal', 'datalim')
    plt.title('Visualization of Embeddings in 2D')
    plt.axis('off')
    plt.show()

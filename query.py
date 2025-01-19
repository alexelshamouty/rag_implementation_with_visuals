import chromadb
import numpy as np
from customEmbeddings import MyCustomEmbedding
from sentence_transformers import CrossEncoder
import heapq

chroma_client = chromadb.PersistentClient(path="./chroma_db/")
chroma_collection = chroma_client.get_collection(name="myRag",embedding_function=MyCustomEmbedding())

def query(query_text: str):
    return chroma_collection.query(query_texts=query_text, n_results=5, include=["documents","embeddings", "distances"])

def return_all_embeddings():
    return chroma_collection.get(include=['embeddings'])['embeddings']

def return_results_embeddings(results):
    return results['embeddings'][0]

def return_results_documents(results):
    return results['documents'][0]

def return_results_distances(results):
    return results['distances'][0]
def document_distance(results: dict):
    return zip(results['documents'][0],results['distances'][0])

def multi_query(queries: list):
    found_embeddings = []
    found_documents = []
    found_distances = []
    for query_string in queries:
        results = query(query_string)
        embeddings = return_results_embeddings(results)
        documents = return_results_documents(results)
        distances = return_results_distances(results)
        found_embeddings += [embedding for embedding in embeddings 
                             if not any(np.array_equal(embedding,found) for found in found_embeddings)
                             ]
        found_documents += [document for document in documents if document not in found_documents ]
        found_distances += [distance for distance in distances if distance not in found_distances ]
    return found_documents, found_embeddings, found_distances

def generate_ranked_results(queries: list):
    found_documents, found_embeddings, found_distances = multi_query(queries)
    cross_encoder = CrossEncoder('cross-encoder/stsb-roberta-large')
    docscore = []

    for query_text in queries:
        for document, embedding, distance in zip(found_documents, found_embeddings, found_distances):
            pair = [query_text, document]
            score = cross_encoder.predict(pair)
            docscore.append((score, 
                             {
                                "document":document,
                                "query_text":query_text,
                                "embeddings":embedding,
                                "distance":distance
                            }
                ))
            
    top_5_list = heapq.nlargest(5, docscore, key=lambda x: x[0])

    top_5_scores = [score for score, document in top_5_list]
    top_5_documents = [document for score, document in top_5_list]

    return top_5_scores, top_5_documents

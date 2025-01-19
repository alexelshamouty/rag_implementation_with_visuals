from sentence_transformers import SentenceTransformer

#Initialise the model and use Hugging Face Embeddings
class MyCustomEmbedding:
    def __init__(self):
        self.model = SentenceTransformer('sentence-transformers/multi-qa-mpnet-base-dot-v1')
    def __call__(self, input):
        return list(self.model.encode(input, conver_to_numpy=True))
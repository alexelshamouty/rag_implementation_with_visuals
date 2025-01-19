from langchain_text_splitters.character import RecursiveCharacterTextSplitter
from customEmbeddings import MyCustomEmbedding
from pypdf import PdfReader
import chromadb
import sys
import logging
from tqdm import tqdm
import warnings

#Reduce the noise a bit
logging.getLogger("pypdf").setLevel(logging.ERROR)
logging.getLogger("sklearn").setLevel(logging.ERROR)
logging.getLogger("umap").setLevel(logging.ERROR)
# Suppress all warnings
warnings.filterwarnings("ignore")

#Initialise Chroma
chroma_client = chromadb.PersistentClient(path="./chroma_db/")
chroma_collection = chroma_client.get_or_create_collection(name="myRag",metadata={"hnsw:space": "cosine"}, embedding_function=MyCustomEmbedding())

    
def read_data(path: str):
    content = PdfReader(path.strip())
    pdftext = [page.extract_text().strip() for page in content.pages if page.extract_text()]
    return pdftext

def split_and_store(data: list):
    splitter = RecursiveCharacterTextSplitter("\n", chunk_size=5000, chunk_overlap=0, length_function = len )
    splits = splitter.split_text("\n\n".join(data))
    for index, text in tqdm(enumerate(splits), total=len(splits), desc="Loading embeddings into Chroma"):
        chroma_collection.add(str(index), documents=text)


# Main Code
def load_embeddings(filename):
    data = read_data(filename)
    split_and_store(data)
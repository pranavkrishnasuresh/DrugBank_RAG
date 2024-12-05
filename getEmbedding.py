# from langchain_community.embeddings.ollama import OllamaEmbeddings

# def get_embedding_function():
#     embeddings = OllamaEmbeddings(
#         embeddings = OllamaEmbeddings(model="nomic-embed-text")
#     )
#     return embeddings

from langchain_community.embeddings.ollama import OllamaEmbeddings

def get_embedding_function():
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    return embeddings

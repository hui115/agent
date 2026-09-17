from langchain_chroma import  Chroma
from langchain_community.embeddings import DashScopeEmbeddings
import config_data
class VectorStoreService(object):
    embedding=None
    vector_store=None
    def __init__(self):
        self.embedding=DashScopeEmbeddings(model='text-embedding-v4')
        self.vector_store = Chroma(
            collection_name=config_data.collection_name,
            embedding_function=self.embedding,
            persist_directory=config_data.persist_directory
        )
    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={'k':config_data.similarity_threshold})

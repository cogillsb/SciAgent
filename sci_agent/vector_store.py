from chromadb import PersistentClient, EmbeddingFunction, Embeddings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from typing import List

MODEL_NAME = "Alibaba-NLP/gte-Qwen2-1.5B-instruct"
DB_PATH = "./.chroma_db"

class Protocol:
    def __init__(self, path: str, text:str):
        self.path = path
        self.text  = text

class CustomEmbeddingClass(EmbeddingFunction):
    def __init__(self, model_name):
        self.embedding_model = HuggingFaceEmbedding(model_name)

    def __call__(self, input_texts: List[str])->Embeddings:
        return [self.embedding_model.get_text_embedding(text) for text in input_texts]
    




db = PersistentClient(path=DB_PATH)

custom_embedding_function = CustomEmbeddingClass(MODEL_NAME)

collection = db.get_or_create_collection(name='SOPs', embedding_function=custom_embedding_function)
print("model done")
#collection.add(
    #documents = 
#)




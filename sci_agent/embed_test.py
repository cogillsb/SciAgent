from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from chromadb import PersistentClient, EmbeddingFunction, Embeddings
import json
from dotenv import load_dotenv


DB_PATH = "./.chroma_db"
db = PersistentClient(path=DB_PATH)



db.delete_collection(name="Protocols")



collection = db.get_or_create_collection(name='FAQ')
collection.add(
    documents=[faq['question'] for faq in faqs] + [faq['answer'] for faq in faqs],
    ids = [str(i) for i in range(0, 2*len(faqs))],
    metadatas= faqs + faqs
)
#print(collection.get(include=['embeddings', 'documents', 'metadatas']))
results = collection.query(
    query_texts=["how do i refresh my protocols"], # Chroma will embed this for you
    n_results=1 # how many results to return
)
print(results)
for c in db.list_collections():
    print(c)


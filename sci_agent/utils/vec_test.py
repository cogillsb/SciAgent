from langchain_text_splitters import RecursiveCharacterTextSplitter
from chromadb import PersistentClient
import json
import os
from docx import Document


DB_PATH = "./.chroma_db"
FAQ_FILE_PATH = "sci_agent\data\\faqs.json"
PROTOCOL_FOLDER_PATH = "sci_agent\data\protocols"

class SciAgentVectoreStore:
    def __init__(self):
        db = PersistentClient(path=DB_PATH)

        self.text_splitter = RecursiveCharacterTextSplitter(            
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len,
                is_separator_regex=False,
            )
        
       
        self.faq_collection = db.get_or_create_collection(name='FAQ')
        self.protocol_collection = db.get_or_create_collection(name="Protocols")


        if self.faq_collection.count() == 0:
            self._load_faq_collection(FAQ_FILE_PATH)
        
        if self.protocol_collection.count() == 0:
            self._load_protocol_collection(PROTOCOL_FOLDER_PATH)
    
    def _load_faq_collection(self, faq_file_path:str):
        with open(faq_file_path, 'r') as f:
            faqs = json.load(f)
        
        self.faq_collection.add(
            documents=[faq['question'] for faq in faqs] + [faq['answer'] for faq in faqs],
            ids = [str(i) for i in range(0, 2*len(faqs))],
            metadatas= faqs + faqs
        )
    
    def _load_protocol_collection(self, directory):

        for root, _, files in os.walk(directory):
            for file in files:          
                file_path = os.path.join(root, file)
                file_name = os.path.splitext(file)[0]
                if file.endswith(".docx"):
                    try:
                        document = Document(file_path)
                        text = []
                        for paragraph in document.paragraphs:
                            text.append(paragraph.text)
                        content = "\n".join(text)                        
                    except Exception as e:
                        print(f"Error opening {file_path}: {e}")
                else:
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                    except Exception as e:
                        print(f"Error opening {file_path}: {e}")
                
                chunks = self.text_splitter.split_text(content)
                documents  = []
                ids = []
                metadatas = []
                for i  in range(len(chunks)):
                    documents.append(chunks[i])
                    ids.append(f"{file_name}_{i}")
                    metadatas.append({
                        'path': file_path,
                        'chunk': i
                    })                
                self.protocol_collection.add(documents=documents, ids=ids, metadatas=metadatas) 
    
    def query_faqs(self, query):
        return self.faq_collection.query(query_texts=[query], n_results=1)
    
    def query_protocols(self, query):
        return self.protocol_collection.query(query_texts=[query], n_results=10)
       
    




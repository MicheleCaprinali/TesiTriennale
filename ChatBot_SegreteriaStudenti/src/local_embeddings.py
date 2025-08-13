"""
Modulo per gestire gli embedding con Sentence Transformers (gratuito)
"""

from sentence_transformers import SentenceTransformer
import os
from typing import List
from dotenv import load_dotenv

load_dotenv()

class LocalEmbeddings:
    """
    Classe per gestire embedding locali con SentenceTransformers
    Completamente gratuito e funziona offline
    """
    
    def __init__(self, model_name: str = None):
        self.model_name = model_name or os.getenv('EMBEDDING_MODEL', 'all-MiniLM-L6-v2')
        print(f"🔄 Caricamento modello di embedding: {self.model_name}")
        self.model = SentenceTransformer(self.model_name)
        print("✅ Modello di embedding caricato!")
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Crea embedding per una lista di documenti"""
        print(f"🔄 Creazione embedding per {len(texts)} documenti...")
        embeddings = self.model.encode(texts, show_progress_bar=True)
        return embeddings.tolist()
    
    def embed_query(self, text: str) -> List[float]:
        """Crea embedding per una singola query"""
        embedding = self.model.encode([text])
        return embedding[0].tolist()

if __name__ == "__main__":
    # Test del modulo
    embedder = LocalEmbeddings()
    
    # Test con documenti di esempio
    test_docs = [
        "Come faccio a iscrivermi agli esami?",
        "Quando devo pagare le tasse universitarie?",
        "Dove trovo il piano di studi?"
    ]
    
    print("\n📝 Test embedding documenti:")
    doc_embeddings = embedder.embed_documents(test_docs)
    print(f"✅ Creati {len(doc_embeddings)} embedding di dimensione {len(doc_embeddings[0])}")
    
    print("\n🔍 Test embedding query:")
    query_embedding = embedder.embed_query("Come mi iscrivo?")
    print(f"✅ Creato embedding query di dimensione {len(query_embedding)}")

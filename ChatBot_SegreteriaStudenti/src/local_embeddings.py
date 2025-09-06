"""
Modulo per gestire gli embedding con Sentence Transformers
Ottimizzato per performance e affidabilità (Settembre 2025)
"""

from sentence_transformers import SentenceTransformer
import os
import numpy as np
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

class LocalEmbeddings:
    """
    Classe per gestire embedding locali con SentenceTransformers
    """

    def __init__(self, model_name: str = None):
        self.model_name = model_name or os.getenv('EMBEDDING_MODEL', 'all-MiniLM-L6-v2')
        print(f"Caricamento modello di embedding: {self.model_name}")
        self.model = SentenceTransformer(self.model_name)
        print("✅ Modello di embedding caricato!")
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Crea embedding per una lista di documenti"""
        print(f"Creazione embedding per {len(texts)} documenti...")
        embeddings = self.model.encode(texts, show_progress_bar=True)
        return embeddings.tolist()
    
    def embed_query(self, text: str) -> List[float]:
        """Crea embedding per una singola query"""
        embedding = self.model.encode([text])
        return embedding[0].tolist()
    
    def get_model_info(self) -> Dict[str, Any]:
        """Ottieni informazioni sul modello di embedding"""
        return {
            "model_name": self.model_name,
            "embedding_size": self.model.get_sentence_embedding_dimension(),
            "max_seq_length": self.model.max_seq_length,
            "device": str(self.model.device),
            "model_type": "SentenceTransformer"
        }
    
    def compute_similarity(self, text1: str, text2: str) -> float:
        """Calcola la similarità coseno tra due testi"""
        emb1 = np.array(self.embed_query(text1))
        emb2 = np.array(self.embed_query(text2))
        
        # Similarità coseno
        cos_sim = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
        return float(cos_sim)

if __name__ == "__main__":
    embedder = LocalEmbeddings()
    
    # Test con documenti di esempio
    test_docs = ["Informazioni segreteria studenti", "Orari uffici universitari"]
    doc_embeddings = embedder.embed_documents(test_docs)
    print(f"Embedding documenti: {len(doc_embeddings)} vettori di dimensione {len(doc_embeddings[0])}")
    
    # Test query
    query_embedding = embedder.embed_query("orari segreteria")
    print(f"Embedding query: vettore di dimensione {len(query_embedding)}")
    
    # Test similarità
    similarity = embedder.compute_similarity("segreteria studenti", "ufficio studenti")
    print(f"Similarità 'segreteria studenti' vs 'ufficio studenti': {similarity:.3f}")
    
    # Info modello
    model_info = embedder.get_model_info()
    print(f"Modello: {model_info['model_name']}")
    print(f"Dimensioni embedding: {model_info['embedding_size']}")
    print(f"Lunghezza massima sequenza: {model_info['max_seq_length']}")
    print(f"Device: {model_info['device']}")
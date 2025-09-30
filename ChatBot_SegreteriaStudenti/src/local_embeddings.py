"""
Modulo per gestire gli embedding con Sentence Transformers
Ottimizzato per performance e affidabilità (Settembre 2025)
"""

from sentence_transformers import SentenceTransformer
import os
import numpy as np
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
import logging

load_dotenv()

# Configurazione logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LocalEmbeddings:
    """
    Classe per gestire embedding locali con SentenceTransformers
    """

    def __init__(self, model_name: Optional[str] = None):
        self.model_name = model_name or os.getenv('EMBEDDING_MODEL', 'all-MiniLM-L6-v2')
        
        try:
            print(f"🔄 Caricamento modello di embedding: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            print("✅ Modello di embedding caricato!")
        except Exception as e:
            logger.error(f"❌ Errore nel caricamento del modello: {e}")
            raise
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """o embedding per una lista di documenti"""
        if not texts:
            logger.warning("⚠️ Lista di testi vuota")
            return []
            
        print(f"🔄 Creazione embedding per {len(texts)} documenti...")
        try:
            embeddings = self.model.encode(texts, show_progress_bar=True, convert_to_tensor=False)
            return embeddings.tolist()
        except Exception as e:
            logger.error(f"❌ Errore nella creazione embedding documenti: {e}")
            raise
    
    def embed_query(self, text: str) -> List[float]:
        """Crea embedding per una singola query"""
        if not text.strip():
            logger.warning("⚠️ Query vuota")
            return []
            
        try:
            embedding = self.model.encode([text], convert_to_tensor=False)
            return embedding[0].tolist()
        except Exception as e:
            logger.error(f"❌ Errore nella creazione embedding query: {e}")
            raise
    
    def get_model_info(self) -> Dict[str, Any]:
        """Ottieni informazioni sul modello di embedding"""
        try:
            return {
                "model_name": self.model_name,
                "embedding_size": self.model.get_sentence_embedding_dimension(),
                "max_seq_length": getattr(self.model, 'max_seq_length', 'N/A'),
                "device": str(self.model.device),
                "model_type": "SentenceTransformer"
            }
        except Exception as e:
            logger.error(f"❌ Errore nel recupero info modello: {e}")
            return {"error": str(e)}
    
    def compute_similarity(self, text1: str, text2: str) -> float:
        """Calcola la similarità coseno tra due testi"""
        try:
            emb1 = np.array(self.embed_query(text1))
            emb2 = np.array(self.embed_query(text2))
            
            if len(emb1) == 0 or len(emb2) == 0:
                return 0.0
            
            # Similarità coseno
            cos_sim = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
            return float(cos_sim)
        except Exception as e:
            logger.error(f"❌ Errore nel calcolo similarità: {e}")
            return 0.0

    def batch_embed_with_metadata(self, texts: List[str], metadata: List[Dict] = None) -> List[Dict]:
        """Crea embedding con metadati associati per ogni chunk"""
        embeddings = self.embed_documents(texts)
        
        results = []
        for i, (text, embedding) in enumerate(zip(texts, embeddings)):
            result = {
                "text": text,
                "embedding": embedding,
                "metadata": metadata[i] if metadata and i < len(metadata) else {"index": i}
            }
            results.append(result)
        
        return results

if __name__ == "__main__":
    try:
        embedder = LocalEmbeddings()
        
        # Test con documenti di esempio
        test_docs = ["Informazioni segreteria studenti", "Orari uffici universitari"]
        doc_embeddings = embedder.embed_documents(test_docs)
        print(f"📊 Embedding documenti: {len(doc_embeddings)} vettori di dimensione {len(doc_embeddings[0])}")
        
        # Test query
        query_embedding = embedder.embed_query("orari segreteria")
        print(f"📊 Embedding query: vettore di dimensione {len(query_embedding)}")
        
        # Test similarità
        similarity = embedder.compute_similarity("segreteria studenti", "ufficio studenti")
        print(f"📊 Similarità 'segreteria studenti' vs 'ufficio studenti': {similarity:.3f}")
        
        # Info modello
        model_info = embedder.get_model_info()
        print(f"🤖 Modello: {model_info['model_name']}")
        print(f"📏 Dimensioni embedding: {model_info['embedding_size']}")
        print(f"📝 Lunghezza massima sequenza: {model_info['max_seq_length']}")
        print(f"💻 Device: {model_info['device']}")
        
    except Exception as e:
        print(f"❌ Errore durante i test: {e}")
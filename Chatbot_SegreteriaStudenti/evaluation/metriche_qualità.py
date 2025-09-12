"""
Sistema di valutazione automatica qualità risposte ChatBot
Versione semplificata senza dipendenze NLTK - Solo SentenceTransformers + built-ins
"""

import re
import math
from typing import Dict, List, Tuple, Any
from collections import Counter
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class ResponseQualityEvaluator:
    """Valutatore qualità risposte - Versione semplificata"""
    
    def __init__(self):
        # Usa il model che hai già per embedding
        self.similarity_model = SentenceTransformer('all-MiniLM-L6-v2')
        
    def evaluate_response(self, 
                         question: str,
                         generated_response: str, 
                         reference_response: str = None,
                         context: str = None) -> Dict[str, float]:
        """Valuta qualità risposta con metriche essenziali"""
        
        metrics = {}
        
        # 1. Metriche di base (lunghezza, struttura)
        metrics.update(self._basic_metrics(generated_response))
        
        # 2. Rilevanza semantica
        metrics.update(self._relevance_metrics(question, generated_response))
        
        # 3. Qualità contenuto
        metrics.update(self._content_quality_metrics(generated_response, context))
        
        # 4. Metriche comparative (se abbiamo riferimento)
        if reference_response:
            metrics.update(self._comparative_metrics(generated_response, reference_response))
        
        # 5. Score finale
        metrics['overall_score'] = self._calculate_overall_score(metrics)
        
        return metrics
    
    def _basic_metrics(self, response: str) -> Dict[str, float]:
        """Metriche di base senza NLTK"""
        
        # Sentence splitting semplice
        sentences = [s.strip() for s in re.split(r'[.!?]+', response) if s.strip()]
        words = response.split()
        
        return {
            'length_words': len(words),
            'length_chars': len(response),
            'num_sentences': len(sentences),
            'avg_sentence_length': len(words) / max(len(sentences), 1),
            'has_links': 1.0 if re.search(r'https?://', response) else 0.0,
            'has_structure': 1.0 if any(marker in response for marker in ['•', '-', '1.', '2.', '\n']) else 0.0
        }
    
    def _relevance_metrics(self, question: str, response: str) -> Dict[str, float]:
        """Metriche rilevanza domanda-risposta"""
        
        # Semantic similarity usando il tuo model
        try:
            q_embedding = self.similarity_model.encode([question])
            r_embedding = self.similarity_model.encode([response])
            semantic_sim = cosine_similarity(q_embedding, r_embedding)[0][0]
        except:
            semantic_sim = 0.5  # Fallback
        
        # Keyword overlap semplice
        q_words = set(re.findall(r'\w+', question.lower()))
        r_words = set(re.findall(r'\w+', response.lower()))
        
        if q_words:
            keyword_overlap = len(q_words & r_words) / len(q_words)
        else:
            keyword_overlap = 0.0
        
        return {
            'semantic_similarity': float(semantic_sim),
            'keyword_overlap': keyword_overlap
        }
    
    def _content_quality_metrics(self, response: str, context: str = None) -> Dict[str, float]:
        """Metriche qualità contenuto"""
        
        metrics = {
            'completeness_score': self._assess_completeness(response),
            'informativeness_score': self._assess_informativeness(response), 
            'clarity_score': self._assess_clarity(response),
            'professional_tone': self._assess_professional_tone(response)
        }
        
        # Context utilization se disponibile
        if context:
            metrics['context_utilization'] = self._assess_context_usage(response, context)
        
        return metrics
    
    def _comparative_metrics(self, generated: str, reference: str) -> Dict[str, float]:
        """Metriche comparative con riferimento"""
        
        # BLEU semplificato
        bleu = self._simple_bleu(generated, reference)
        
        # Semantic similarity con riferimento
        try:
            g_embed = self.similarity_model.encode([generated])
            r_embed = self.similarity_model.encode([reference])
            ref_similarity = cosine_similarity(g_embed, r_embed)[0][0]
        except:
            ref_similarity = 0.5
        
        return {
            'bleu_score': bleu,
            'reference_similarity': float(ref_similarity)
        }
    
    def _assess_completeness(self, response: str) -> float:
        """Valuta completezza della risposta"""
        
        score = 0.0
        word_count = len(response.split())
        
        # Lunghezza appropriata (30-400 parole)
        if 30 <= word_count <= 400:
            score += 0.4
        elif word_count >= 15:
            score += 0.2
        
        # Presenza dettagli procedurali
        if any(term in response.lower() for term in ['procedura', 'passo', 'fase', 'primo', 'secondo']):
            score += 0.3
        
        # Informazioni di contatto
        if any(info in response.lower() for info in ['contatto', 'segreteria', 'http', 'email']):
            score += 0.3
        
        return min(score, 1.0)
    
    def _assess_informativeness(self, response: str) -> float:
        """Valuta informatività"""
        
        score = 0.0
        
        # Termini specifici UniBg
        unibg_terms = ['università', 'bergamo', 'unibg', 'segreteria', 'studenti']
        found_terms = sum(1 for term in unibg_terms if term in response.lower())
        score += min(found_terms * 0.1, 0.4)
        
        # Informazioni concrete (numeri, orari)
        if re.search(r'\b\d+\b', response):
            score += 0.2
        
        # Evita risposte generiche
        generic_phrases = ['non ho informazioni', 'contatta la segreteria', 'informazioni insufficienti']
        if any(phrase in response.lower() for phrase in generic_phrases):
            score = max(score - 0.3, 0.0)
        else:
            score += 0.4
        
        return min(score, 1.0)
    
    def _assess_clarity(self, response: str) -> float:
        """Valuta chiarezza"""
        
        score = 0.0
        sentences = [s.strip() for s in re.split(r'[.!?]+', response) if s.strip()]
        
        if sentences:
            avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences)
            
            # Lunghezza frasi appropriate
            if 8 <= avg_sentence_length <= 25:
                score += 0.4
            elif avg_sentence_length <= 30:
                score += 0.2
        
        # Presenza di struttura (liste, punti)
        if any(marker in response for marker in ['•', '\n-', '1.', '2.']):
            score += 0.3
        
        # Formatting markdown
        if any(fmt in response for fmt in ['**', '__', '\n']):
            score += 0.3
        
        return min(score, 1.0)
    
    def _assess_professional_tone(self, response: str) -> float:
        """Valuta tono professionale"""
        
        score = 0.7  # Base score
        
        # Tono cordiale ma formale
        if any(phrase in response.lower() for phrase in ['gentilmente', 'prego', 'cordiali']):
            score += 0.2
        
        # Evita tono informale
        informal_words = ['ciao', 'hey', 'ok', 'boh', 'tipo']
        for word in informal_words:
            if word in response.lower():
                score -= 0.1
        
        return max(min(score, 1.0), 0.0)
    
    def _assess_context_usage(self, response: str, context: str) -> float:
        """Valuta utilizzo del contesto"""
        
        if not context:
            return 0.0
        
        try:
            r_embed = self.similarity_model.encode([response])
            c_embed = self.similarity_model.encode([context])
            context_sim = cosine_similarity(r_embed, c_embed)[0][0]
            return float(context_sim)
        except:
            return 0.5
    
    def _simple_bleu(self, generated: str, reference: str) -> float:
        """BLEU semplificato"""
        
        gen_words = generated.lower().split()
        ref_words = reference.lower().split()
        
        if not gen_words or not ref_words:
            return 0.0
        
        # 1-gram precision
        gen_counter = Counter(gen_words)
        ref_counter = Counter(ref_words)
        
        overlap = sum((gen_counter & ref_counter).values())
        precision = overlap / len(gen_words) if gen_words else 0.0
        
        # Length penalty
        length_penalty = min(1.0, len(gen_words) / len(ref_words)) if ref_words else 0.0
        
        return precision * length_penalty
    
    def _calculate_overall_score(self, metrics: Dict[str, float]) -> float:
        """Score complessivo"""
        
        # Pesi semplificati
        weights = {
            'semantic_similarity': 0.3,    # 30% rilevanza
            'completeness_score': 0.2,     # 20% completezza  
            'informativeness_score': 0.2,  # 20% informatività
            'clarity_score': 0.15,         # 15% chiarezza
            'professional_tone': 0.15,     # 15% professionalità
        }
        
        score = 0.0
        total_weight = 0.0
        
        for metric, weight in weights.items():
            if metric in metrics:
                score += metrics[metric] * weight
                total_weight += weight
        
        return round(score / total_weight if total_weight > 0 else 0.0, 3)

# Funzione helper semplificata
def evaluate_chatbot_response(question: str, response: str, context: str = None) -> Dict[str, Any]:
    """Funzione principale per valutare una risposta"""
    
    evaluator = ResponseQualityEvaluator()
    metrics = evaluator.evaluate_response(question, response, context=context)
    
    def score_to_label(score):
        if score >= 0.8: return "Eccellente"
        elif score >= 0.6: return "Buono"
        elif score >= 0.4: return "Sufficiente"  
        else: return "Da Migliorare"
    
    return {
        'metrics': metrics,
        'quality_label': score_to_label(metrics['overall_score']),
        'main_areas': {
            'rilevanza': score_to_label(metrics.get('semantic_similarity', 0)),
            'completezza': score_to_label(metrics.get('completeness_score', 0)),
            'chiarezza': score_to_label(metrics.get('clarity_score', 0))
        }
    }

# Test
if __name__ == "__main__":
    question = "Come faccio a iscrivermi agli esami?"
    response = """Per iscriverti agli esami all'Università di Bergamo:

• Accedi al portale studenti online
• Vai nella sezione "Iscrizioni esami"
• Seleziona l'esame desiderato
• Conferma entro le scadenze

Le iscrizioni aprono 15 giorni prima dell'esame."""
    
    result = evaluate_chatbot_response(question, response)
    
    print("📊 VALUTAZIONE RISPOSTA")
    print("=" * 30)
    print(f"Overall Score: {result['metrics']['overall_score']}")
    print(f"Quality: {result['quality_label']}")
    print(f"\nDettagli:")
    for area, quality in result['main_areas'].items():
        print(f"  {area}: {quality}")
"""
Valutazione automatica qualità risposte ChatBot per tesi
Usa SentenceTransformers per analisi semantica
"""

import re
from typing import Dict, Any, List, Tuple
from collections import Counter
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json
from pathlib import Path

# Importazioni opzionali per metriche avanzate RAG
try:
    import nltk
    from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False

try:
    from rouge_score import rouge_scorer
    ROUGE_AVAILABLE = True
except ImportError:
    ROUGE_AVAILABLE = False

class ResponseQualityEvaluator:
    """Valutatore qualità risposte ChatBot"""
    
    def __init__(self):
        # Usa modello SentenceTransformers per similarità semantica
        self.similarity_model = SentenceTransformer('all-MiniLM-L6-v2')
        
    def evaluate_response(self, 
                         question: str,
                         generated_response: str, 
                         reference_response: str = None,
                         context: str = None) -> Dict[str, float]:
        """Valuta qualità risposta con metriche essenziali"""
        
        metrics = {}
        
        # Metriche di base (lunghezza, struttura)
        metrics.update(self._basic_metrics(generated_response))
        
        # Rilevanza semantica domanda-risposta
        metrics.update(self._relevance_metrics(question, generated_response))
        
        # Qualità contenuto specifico
        metrics.update(self._content_quality_metrics(generated_response, context))
        
        # Metriche comparative con riferimento
        if reference_response:
            metrics.update(self._comparative_metrics(generated_response, reference_response))
        
        # Score finale complessivo
        metrics['overall_score'] = self._calculate_overall_score(metrics)
        
        return metrics
    
    def _basic_metrics(self, response: str) -> Dict[str, float]:
        """Metriche di base struttura risposta"""
        
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
        
        # Similarità semantica con SentenceTransformers
        try:
            q_embedding = self.similarity_model.encode([question])
            r_embedding = self.similarity_model.encode([response])
            semantic_sim = cosine_similarity(q_embedding, r_embedding)[0][0]
        except:
            semantic_sim = 0.5  # Fallback
        
        # Overlap keyword semplice
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
        
        # Utilizzo contesto se disponibile
        if context:
            metrics['context_utilization'] = self._assess_context_usage(response, context)
        
        return metrics
    
    def _comparative_metrics(self, generated: str, reference: str) -> Dict[str, float]:
        """Metriche comparative con risposta di riferimento"""
        
        # BLEU semplificato
        bleu = self._simple_bleu(generated, reference)
        
        # Similarità semantica con riferimento
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
        """Valuta informatività e specificità della risposta"""
        
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
        """Valuta chiarezza e leggibilità"""
        
        score = 0.0
        sentences = [s.strip() for s in re.split(r'[.!?]+', response) if s.strip()]
        
        if sentences:
            avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences)
            
            # Lunghezza frasi appropriate (8-25 parole)
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
        
        score = 0.7  # Score base
        
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
        """Calcola score complessivo con pesi bilanciati"""
        
        # Pesi per diverse dimensioni di qualità
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


class RAGSystemEvaluator:
    """Valutatore specifico per sistemi RAG (Retrieval-Augmented Generation)"""
    
    def __init__(self):
        self.similarity_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.smoothing_function = None
        if NLTK_AVAILABLE:
            self.smoothing_function = SmoothingFunction().method1
        
    def evaluate_rag_system(self, 
                           query: str,
                           generated_response: str,
                           reference_response: str,
                           retrieved_documents: List[str],
                           relevant_documents: List[str] = None,
                           k_values: List[int] = [1, 3, 5]) -> Dict[str, float]:
        """
        Valuta sistema RAG con metriche specifiche
        
        Args:
            query: Domanda dell'utente
            generated_response: Risposta generata dal sistema
            reference_response: Risposta di riferimento (ground truth)
            retrieved_documents: Documenti recuperati dal sistema
            relevant_documents: Documenti effettivamente rilevanti (per Recall@K)
            k_values: Valori di K per calcolare Recall@K
        """
        
        metrics = {}
        
        # 1. Recall@K - Valuta capacità di retrieval
        if relevant_documents:
            metrics.update(self._calculate_recall_at_k(retrieved_documents, relevant_documents, k_values))
        
        # 2. BLEU Score - Similarità n-gram con riferimento
        metrics['bleu_score'] = self._calculate_bleu_score(generated_response, reference_response)
        
        # 3. ROUGE-L - Sovrapposizione sequenze lunghe
        metrics['rouge_l'] = self._calculate_rouge_l(generated_response, reference_response)
        
        # 4. BERTScore (semantica) - Usando SentenceTransformers
        metrics['bert_score'] = self._calculate_bert_score(generated_response, reference_response)
        
        # 5. Answer Relevance - Rilevanza risposta alla domanda
        metrics['answer_relevance'] = self._calculate_answer_relevance(query, generated_response)
        
        # 6. Context Precision - Quanto il contesto recuperato è preciso
        if retrieved_documents and relevant_documents:
            metrics['context_precision'] = self._calculate_context_precision(retrieved_documents, relevant_documents)
        
        # 7. Faithfulness - Quanto la risposta è fedele al contesto
        if retrieved_documents:
            metrics['faithfulness'] = self._calculate_faithfulness(generated_response, retrieved_documents)
        
        # Score RAG complessivo
        metrics['rag_overall_score'] = self._calculate_rag_overall_score(metrics)
        
        return metrics
    
    def _calculate_recall_at_k(self, retrieved_docs: List[str], relevant_docs: List[str], k_values: List[int]) -> Dict[str, float]:
        """Calcola Recall@K per diversi valori di K"""
        
        recall_metrics = {}
        
        for k in k_values:
            if k <= len(retrieved_docs):
                top_k_retrieved = set(retrieved_docs[:k])
                relevant_set = set(relevant_docs)
                
                # Calcola quanti documenti rilevanti sono nei top-K
                relevant_in_top_k = len(top_k_retrieved.intersection(relevant_set))
                total_relevant = len(relevant_set)
                
                recall_at_k = relevant_in_top_k / total_relevant if total_relevant > 0 else 0.0
                recall_metrics[f'recall_at_{k}'] = round(recall_at_k, 3)
            else:
                recall_metrics[f'recall_at_{k}'] = 0.0
        
        return recall_metrics
    
    def _calculate_bleu_score(self, generated: str, reference: str) -> float:
        """Calcola BLEU score avanzato"""
        
        if NLTK_AVAILABLE:
            try:
                # Tokenizzazione semplice
                gen_tokens = generated.lower().split()
                ref_tokens = [reference.lower().split()]  # Lista di liste per NLTK
                
                # Calcola BLEU con smoothing
                bleu = sentence_bleu(ref_tokens, gen_tokens, smoothing_function=self.smoothing_function)
                return round(bleu, 3)
            except:
                pass
        
        # Fallback BLEU semplificato
        return self._simple_bleu_fallback(generated, reference)
    
    def _calculate_rouge_l(self, generated: str, reference: str) -> float:
        """Calcola ROUGE-L score"""
        
        if ROUGE_AVAILABLE:
            try:
                scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
                scores = scorer.score(reference, generated)
                return round(scores['rougeL'].fmeasure, 3)
            except:
                pass
        
        # Fallback ROUGE-L semplificato
        return self._simple_rouge_l_fallback(generated, reference)
    
    def _calculate_bert_score(self, generated: str, reference: str) -> float:
        """Calcola BERTScore usando SentenceTransformers"""
        
        try:
            gen_embedding = self.similarity_model.encode([generated])
            ref_embedding = self.similarity_model.encode([reference])
            
            # Similarità coseno come proxy per BERTScore
            bert_score = cosine_similarity(gen_embedding, ref_embedding)[0][0]
            return round(float(bert_score), 3)
        except:
            return 0.5
    
    def _calculate_answer_relevance(self, query: str, answer: str) -> float:
        """Calcola rilevanza della risposta alla domanda"""
        
        try:
            query_embedding = self.similarity_model.encode([query])
            answer_embedding = self.similarity_model.encode([answer])
            
            relevance = cosine_similarity(query_embedding, answer_embedding)[0][0]
            return round(float(relevance), 3)
        except:
            return 0.5
    
    def _calculate_context_precision(self, retrieved_docs: List[str], relevant_docs: List[str]) -> float:
        """Calcola precisione del contesto recuperato"""
        
        if not retrieved_docs:
            return 0.0
        
        retrieved_set = set(retrieved_docs)
        relevant_set = set(relevant_docs)
        
        # Precision = Documenti rilevanti recuperati / Totale documenti recuperati
        relevant_retrieved = len(retrieved_set.intersection(relevant_set))
        precision = relevant_retrieved / len(retrieved_set)
        
        return round(precision, 3)
    
    def _calculate_faithfulness(self, response: str, context_docs: List[str]) -> float:
        """Calcola fedeltà della risposta al contesto"""
        
        if not context_docs:
            return 0.0
        
        try:
            # Concatena il contesto
            full_context = " ".join(context_docs)
            
            # Calcola similarità semantica
            response_embedding = self.similarity_model.encode([response])
            context_embedding = self.similarity_model.encode([full_context])
            
            faithfulness = cosine_similarity(response_embedding, context_embedding)[0][0]
            return round(float(faithfulness), 3)
        except:
            return 0.5
    
    def _simple_bleu_fallback(self, generated: str, reference: str) -> float:
        """BLEU semplificato senza NLTK"""
        
        gen_words = generated.lower().split()
        ref_words = reference.lower().split()
        
        if not gen_words or not ref_words:
            return 0.0
        
        # 1-gram e 2-gram precision
        gen_1grams = Counter(gen_words)
        ref_1grams = Counter(ref_words)
        
        gen_2grams = Counter(zip(gen_words[:-1], gen_words[1:]))
        ref_2grams = Counter(zip(ref_words[:-1], ref_words[1:]))
        
        # Precision 1-gram
        overlap_1 = sum((gen_1grams & ref_1grams).values())
        precision_1 = overlap_1 / len(gen_words) if gen_words else 0.0
        
        # Precision 2-gram
        overlap_2 = sum((gen_2grams & ref_2grams).values())
        precision_2 = overlap_2 / max(len(gen_words) - 1, 1) if len(gen_words) > 1 else 0.0
        
        # BLEU media geometrica semplificata
        avg_precision = (precision_1 + precision_2) / 2
        
        # Brevity penalty
        bp = min(1.0, len(gen_words) / len(ref_words)) if ref_words else 0.0
        
        return round(avg_precision * bp, 3)
    
    def _simple_rouge_l_fallback(self, generated: str, reference: str) -> float:
        """ROUGE-L semplificato"""
        
        gen_words = generated.lower().split()
        ref_words = reference.lower().split()
        
        if not gen_words or not ref_words:
            return 0.0
        
        # Trova la sottosequenza comune più lunga
        lcs_length = self._lcs_length(gen_words, ref_words)
        
        # ROUGE-L = F1 basato su LCS
        precision = lcs_length / len(gen_words) if gen_words else 0.0
        recall = lcs_length / len(ref_words) if ref_words else 0.0
        
        if precision + recall == 0:
            return 0.0
        
        f1 = (2 * precision * recall) / (precision + recall)
        return round(f1, 3)
    
    def _lcs_length(self, seq1: List[str], seq2: List[str]) -> int:
        """Calcola lunghezza sottosequenza comune più lunga"""
        
        m, n = len(seq1), len(seq2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if seq1[i-1] == seq2[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        
        return dp[m][n]
    
    def _calculate_rag_overall_score(self, metrics: Dict[str, float]) -> float:
        """Calcola score RAG complessivo"""
        
        # Pesi per metriche RAG
        rag_weights = {
            'bleu_score': 0.2,        # 20% - Qualità linguistica
            'rouge_l': 0.15,          # 15% - Sovrapposizione sequenze
            'bert_score': 0.25,       # 25% - Similarità semantica
            'answer_relevance': 0.2,   # 20% - Rilevanza alla domanda
            'context_precision': 0.1,  # 10% - Precisione retrieval
            'faithfulness': 0.1,       # 10% - Fedeltà al contesto
        }
        
        score = 0.0
        total_weight = 0.0
        
        for metric, weight in rag_weights.items():
            if metric in metrics:
                score += metrics[metric] * weight
                total_weight += weight
        
        # Aggiungi bonus per recall se disponibile
        recall_keys = [k for k in metrics.keys() if k.startswith('recall_at_')]
        if recall_keys:
            avg_recall = sum(metrics[k] for k in recall_keys) / len(recall_keys)
            score += avg_recall * 0.1  # 10% bonus per recall
            total_weight += 0.1
        
        return round(score / total_weight if total_weight > 0 else 0.0, 3)


# Funzione helper per valutazione RAG completa
def evaluate_rag_response(query: str, 
                         generated_response: str, 
                         reference_response: str,
                         retrieved_documents: List[str] = None,
                         relevant_documents: List[str] = None,
                         save_to_results: bool = False) -> Dict[str, Any]:
    """Funzione principale per valutare sistema RAG"""
    
    # Valutazione qualità standard
    quality_evaluator = ResponseQualityEvaluator()
    quality_metrics = quality_evaluator.evaluate_response(query, generated_response, reference_response)
    
    # Valutazione RAG specifica
    rag_evaluator = RAGSystemEvaluator()
    rag_metrics = rag_evaluator.evaluate_rag_system(
        query=query,
        generated_response=generated_response,
        reference_response=reference_response,
        retrieved_documents=retrieved_documents or [],
        relevant_documents=relevant_documents
    )
    
    # Combina i risultati
    combined_result = {
        'query': query,
        'generated_response': generated_response,
        'reference_response': reference_response,
        'quality_metrics': quality_metrics,
        'rag_metrics': rag_metrics,
        'overall_quality_score': quality_metrics['overall_score'],
        'overall_rag_score': rag_metrics['rag_overall_score']
    }
    
    # Salvataggio risultati
    if save_to_results:
        results_dir = Path("../results")
        results_dir.mkdir(exist_ok=True)
        
        import time
        detailed_report = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'analysis_type': 'Valutazione Sistema RAG',
            'scope': 'Sistema ChatBot completo con metriche RAG',
            'evaluation_data': combined_result,
            'metrics_summary': {
                'bleu_score': rag_metrics.get('bleu_score', 0),
                'rouge_l': rag_metrics.get('rouge_l', 0),
                'bert_score': rag_metrics.get('bert_score', 0),
                'answer_relevance': rag_metrics.get('answer_relevance', 0),
                'context_precision': rag_metrics.get('context_precision', 0),
                'faithfulness': rag_metrics.get('faithfulness', 0),
                'overall_rag_score': rag_metrics['rag_overall_score']
            }
        }
        
        # Aggiungi recall metrics se disponibili
        recall_summary = {k: v for k, v in rag_metrics.items() if k.startswith('recall_at_')}
        if recall_summary:
            detailed_report['metrics_summary']['recall_metrics'] = recall_summary
        
        output_file = results_dir / 'metriche_rag_results.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(detailed_report, f, indent=2, ensure_ascii=False)
        
        print(f"Report valutazione RAG salvato in: {output_file}")
    
    return combined_result

# Funzione helper per valutazione
def evaluate_chatbot_response(question: str, response: str, context: str = None, save_to_results: bool = False) -> Dict[str, Any]:
    """Funzione principale per valutare una risposta del chatbot"""
    
    evaluator = ResponseQualityEvaluator()
    metrics = evaluator.evaluate_response(question, response, context=context)
    
    def score_to_label(score):
        if score >= 0.8: return "Eccellente"
        elif score >= 0.6: return "Buono"
        elif score >= 0.4: return "Sufficiente"  
        else: return "Da Migliorare"
    
    result = {
        'metrics': metrics,
        'quality_label': score_to_label(metrics['overall_score']),
        'main_areas': {
            'rilevanza': score_to_label(metrics.get('semantic_similarity', 0)),
            'completezza': score_to_label(metrics.get('completeness_score', 0)),
            'chiarezza': score_to_label(metrics.get('clarity_score', 0))
        }
    }
    
    # Salva nella cartella results se richiesto
    if save_to_results:
        from pathlib import Path
        import json
        import time
        
        results_dir = Path("../results")
        results_dir.mkdir(exist_ok=True)
        
        detailed_report = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'analysis_type': 'Valutazione Qualità Risposta',
            'scope': 'Sistema ChatBot completo (main.py, src/, interfaccia/streamlit.py)',
            'question': question,
            'response': response,
            'context': context,
            'evaluation_result': result
        }
        
        output_file = results_dir / 'metriche_qualita_results.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(detailed_report, f, indent=2, ensure_ascii=False)
        
        print(f"Report qualità salvato in: {output_file}")
    
    return result

# Test esempio
if __name__ == "__main__":
    # Test qualità risposta standard
    question = "Come faccio a iscrivermi agli esami?"
    response = """Per iscriverti agli esami all'Università di Bergamo:

• Accedi al portale studenti online
• Vai nella sezione "Iscrizioni esami"
• Seleziona l'esame desiderato
• Conferma entro le scadenze

Le iscrizioni aprono 15 giorni prima dell'esame."""
    
    print("=== VALUTAZIONE QUALITÀ RISPOSTA ===")
    result = evaluate_chatbot_response(question, response, save_to_results=True)
    print(f"Overall Score: {result['metrics']['overall_score']}")
    print(f"Quality: {result['quality_label']}")
    print(f"Dettagli:")
    for area, quality in result['main_areas'].items():
        print(f"  {area}: {quality}")
    
    print("\n=== VALUTAZIONE SISTEMA RAG ===")
    
    # Test RAG con dati di esempio
    rag_query = "Quali documenti servono per l'immatricolazione?"
    rag_response = """Per l'immatricolazione all'Università di Bergamo servono:

• Diploma di maturità originale
• Certificato di nascita
• Documento di identità valido
• Codice fiscale
• 2 foto tessera

Tutti i documenti devono essere presentati presso la Segreteria Studenti."""
    
    rag_reference = """I documenti necessari per l'immatricolazione sono: diploma di scuola superiore, documento d'identità, codice fiscale, certificato di nascita e fotografie formato tessera. La documentazione va consegnata in Segreteria."""
    
    # Simula documenti recuperati dal sistema
    retrieved_docs = [
        "Documento 1: Requisiti immatricolazione - diploma maturità richiesto",
        "Documento 2: Lista documenti - identità, codice fiscale, foto tessera",
        "Documento 3: Procedure segreteria - consegna documenti presso uffici",
        "Documento 4: Orari uffici - apertura al pubblico",
        "Documento 5: Modulistica - form iscrizione online"
    ]
    
    # Documenti effettivamente rilevanti
    relevant_docs = [
        "Documento 1: Requisiti immatricolazione - diploma maturità richiesto",
        "Documento 2: Lista documenti - identità, codice fiscale, foto tessera", 
        "Documento 3: Procedure segreteria - consegna documenti presso uffici"
    ]
    
    # Valutazione RAG completa
    rag_result = evaluate_rag_response(
        query=rag_query,
        generated_response=rag_response,
        reference_response=rag_reference,
        retrieved_documents=retrieved_docs,
        relevant_documents=relevant_docs,
        save_to_results=True
    )
    
    print(f"RAG Overall Score: {rag_result['overall_rag_score']}")
    print(f"Quality Overall Score: {rag_result['overall_quality_score']}")
    print(f"\nMetriche RAG dettagliate:")
    for metric, value in rag_result['rag_metrics'].items():
        if not metric.endswith('_score'):
            print(f"  {metric}: {value}")
    
    print(f"\nBLEU Score: {rag_result['rag_metrics'].get('bleu_score', 'N/A')}")
    print(f"ROUGE-L: {rag_result['rag_metrics'].get('rouge_l', 'N/A')}")
    print(f"BERT Score: {rag_result['rag_metrics'].get('bert_score', 'N/A')}")
    print(f"Answer Relevance: {rag_result['rag_metrics'].get('answer_relevance', 'N/A')}")
    
    recall_metrics = {k: v for k, v in rag_result['rag_metrics'].items() if k.startswith('recall_at_')}
    if recall_metrics:
        print(f"\nRecall Metrics:")
        for k, v in recall_metrics.items():
            print(f"  {k}: {v}")
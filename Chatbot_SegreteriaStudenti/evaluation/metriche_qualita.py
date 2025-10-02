import re
import sys
import os
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

REFERENCE_DATASET = [
    {
        "query": "Come faccio a iscrivermi all'università?",
        "reference_answer": """Per iscriverti all'Università di Bergamo devi seguire questi passi:

1. Consulta l'offerta formativa su https://www.unibg.it/studiare/corsi/offerta-formativa
2. Verifica le scadenze di iscrizione su https://www.unibg.it/studia-noi/iscriversi/scadenze-iscriversi
3. Per corsi ad accesso programmato, consulta i bandi specifici
4. Effettua la pre-iscrizione/immatricolazione online tramite il portale studenti

Le procedure sono diverse per corsi triennali e magistrali. Per informazioni dettagliate: https://www.unibg.it/studia-noi/iscriversi/passi-iscriversi""",
        "relevant_docs": ["iscrizioni_anno_accademico.txt", "guida_dello_studente"],
        "category": "iscrizioni"
    },
    {
        "query": "Quali tasse devo pagare per l'iscrizione?",
        "reference_answer": """All'immatricolazione paghi un contributo fisso di 156€ (tassa regionale + imposta di bollo).

Successivamente pagherai il contributo onnicomprensivo diviso in due rate, il cui importo dipende da:
- Corso di laurea
- Tipologia di iscrizione (tempo pieno/part-time)
- Valore ISEEU (fascia di reddito)

L'ISEEU va richiesto entro il 31 dicembre, altrimenti vieni inserito nella fascia più alta. Per studenti con ISEEU tra 0€ e 26.000€ è previsto l'esonero totale.

Informazioni dettagliate su: https://www.unibg.it/servizi/segreteria/tasse-e-agevolazioni""",
        "relevant_docs": ["tasse.txt", "guida_dello_studente"],
        "category": "tasse"
    },
    {
        "query": "Dove trovo gli orari delle lezioni?",
        "reference_answer": """Gli orari delle lezioni sono disponibili su: https://logistica.unibg.it/PortaleStudenti/

Tramite questo portale puoi anche:
- Visualizzare le date degli appelli d'esame
- Prenotare un posto in aula per lezioni in presenza""",
        "relevant_docs": ["lezioni_esami.txt"],
        "category": "lezioni"
    },
    {
        "query": "Come mi iscrivo agli esami?",
        "reference_answer": """Per iscriverti agli esami:

1. Accedi al portale studenti (Sportello Internet Studenti)
2. Vai nella sezione "Iscrizioni esami"
3. Seleziona l'esame desiderato
4. Conferma l'iscrizione entro la scadenza

Le iscrizioni aprono 15 giorni prima della data dell'esame. Le date degli appelli sono su: https://logistica.unibg.it/PortaleStudenti/""",
        "relevant_docs": ["lezioni_esami.txt", "guida_dello_studente"],
        "category": "esami"
    },
    {
        "query": "Come richiedere un certificato di laurea?",
        "reference_answer": """Per richiedere certificati o transcript of records:

1. Accedi alla Guida Studenti - Rilascio certificati: https://elearning15.unibg.it/mod/book/view.php?id=593&chapterid=240
2. Segui la procedura online tramite Sportello Internet Studenti
3. Puoi richiedere il ritiro presso la Segreteria (su appuntamento) o la spedizione a domicilio

La pergamena di laurea originale viene notificata via email quando pronta.""",
        "relevant_docs": ["richiesta_attestati_documenti.txt", "lauree.txt"],
        "category": "certificati"
    },
    {
        "query": "Quando è la prossima sessione di laurea?",
        "reference_answer": """Le date delle sessioni di laurea e le scadenze per le iscrizioni sono riportate sul Calendario Didattico di ogni Dipartimento.

Per laurearti devi:
1. Presentare eventuale domanda provvisoria (solo per alcuni corsi - verifica sul calendario)
2. Compilare la domanda definitiva di laurea online tramite Sportello Internet
3. Caricare la tesi in PDF entro la scadenza prevista
4. Consegnare una copia cartacea al relatore e correlatore

Guida completa: https://www.unibg.it/sites/default/files/campus_e_servizi/2019_newsite_domanda-conseguimento-titolo_guida_studenti_sintetica.pdf""",
        "relevant_docs": ["lauree.txt", "guida_dello_studente"],
        "category": "laurea"
    },
    {
        "query": "Cos'è l'ISEEU e come lo richiedo?",
        "reference_answer": """L'ISEEU (Indicatore della Situazione Economica Equivalente Universitaria) determina la fascia di reddito per il calcolo delle tasse universitarie.

Come richiederlo:
- Presso qualsiasi CAF (Centro Assistenza Fiscale)
- Online dal Portale unico ISEE dell'INPS: https://servizi2.inps.it/servizi/PortaleUnicoISEE/

Scadenza: 31 dicembre
Se non lo presenti entro la scadenza, verrai inserito automaticamente nella fascia di reddito più alta.

Con ISEEU tra 0€ e 26.000€ hai diritto all'esonero totale delle tasse (con requisiti CFU per anni successivi al primo).""",
        "relevant_docs": ["tasse.txt"],
        "category": "tasse"
    },
    {
        "query": "Ho sostenuto il TOLC l'anno scorso, è ancora valido?",
        "reference_answer": """Sì, per l'anno accademico 2024/2025 sono validi i TOLC sostenuti a partire dal 1° gennaio 2023.

Puoi sostenere il TOLC presso qualsiasi Università (non solo UniBG). Ricorda di effettuare la pre-iscrizione/immatricolazione in UNIBG entro le scadenze previste: il TOLC sostenuto altrove verrà acquisito automaticamente dal sistema.""",
        "relevant_docs": ["iscrizioni_anno_accademico.txt"],
        "category": "iscrizioni"
    },
    {
        "query": "Posso iscrivermi part-time?",
        "reference_answer": """Sì, puoi iscriverti con regime di studio part-time se sei in possesso dei requisiti previsti dal Regolamento di Ateneo: https://www.unibg.it/ateneo/amministrazione/statuto-e-regolamenti/regolamenti/studenti

Se sei già iscritto e vuoi passare da part-time a tempo pieno (o viceversa), consulta la Guida studenti: https://elearning15.unibg.it/mod/book/view.php?id=592&chapterid=126

Nota: lo stato occupazionale "Lavoratore" non determina l'iscrizione part-time, rileva solo ai fini statistici.""",
        "relevant_docs": ["iscrizioni_anno_accademico.txt", "tasse.txt"],
        "category": "iscrizioni"
    },
    {
        "query": "Esistono agevolazioni sulle tasse universitarie?",
        "reference_answer": """Sì, esistono varie tipologie di agevolazioni ed esoneri totali o parziali:

- Esonero totale per ISEEU tra 0€ e 26.000€ (con requisiti CFU)
- Riduzioni in base al valore ISEEU
- Agevolazioni per particolari condizioni (disabilità, merito, ecc.)

Puoi utilizzare il simulatore online per calcolare l'importo dovuto in base al tuo ISEEU.

Informazioni complete su: https://www.unibg.it/studiare/iscriversi/tasse-e-agevolazioni/contribuzione-studentesca""",
        "relevant_docs": ["tasse.txt"],
        "category": "tasse"
    },
    {
        "query": "Cosa succede se non pago le tasse entro la scadenza?",
        "reference_answer": """Il pagamento di una rata oltre la scadenza prevista comporta l'addebito di un importo di mora in base ai giorni di ritardo.

Il bollettino con la mora viene generato automaticamente dal sistema dopo il pagamento della rata scaduta.

Per la seconda rata (scadenza 15 maggio) è possibile richiedere la rateizzazione. Consulta: https://www.unibg.it/studiare/iscriversi/tasse-e-agevolazioni/contribuzione-studentesca/modalita-pagamento

Dettagli sui pagamenti tardivi: https://www.unibg.it/studiare/iscriversi/tasse-e-agevolazioni/contribuzione-studentesca/pagamenti-tardivi""",
        "relevant_docs": ["tasse.txt"],
        "category": "tasse"
    },
    {
        "query": "Esiste un servizio di orientamento?",
        "reference_answer": """Sì, è attivo un servizio di orientamento e tutorato per dubbi e chiarimenti.

Informazioni complete su: https://www.unibg.it/studia-noi/ti-aiutiamo/orientarsi/pot-piani-orientamento-e-tutorato

Il servizio ti può aiutare con:
- Scelta del corso di laurea
- Informazioni sulle procedure di iscrizione
- Supporto durante il percorso universitario""",
        "relevant_docs": ["iscrizioni_anno_accademico.txt", "servizio_orientamento.txt"],
        "category": "servizi"
    },
    {
        "query": "Come posso rateizzare le tasse universitarie?",
        "reference_answer": """Per la seconda rata di contributo onnicomprensivo (scadenza 15 maggio) è possibile richiedere la rateizzazione.

Modalità di pagamento e rateizzazione: https://www.unibg.it/studiare/iscriversi/tasse-e-agevolazioni/contribuzione-studentesca/modalita-pagamento

Se il totale dovuto in base al tuo ISEEU è maggiore di 400€, avrai una seconda rata data dalla differenza tra l'importo dovuto e l'acconto di 400€ già versato.""",
        "relevant_docs": ["tasse.txt"],
        "category": "tasse"
    },
    {
        "query": "Non riesco a laurearmi nella sessione prevista, cosa faccio?",
        "reference_answer": """Se non riesci a laurearti nella sessione per cui hai compilato la domanda:

1. Comunica SUBITO alla Segreteria Studenti tramite ticket
2. La Segreteria annullerà la tua domanda di laurea
3. Dovrai ricompilare la domanda da capo per la sessione successiva

Guida annullamento domanda: https://elearning15.unibg.it/mod/book/view.php?id=593&chapterid=251

Se prevedi di laurearti nella sessione straordinaria di marzo/aprile, non sei tenuto a rinnovare l'iscrizione e pagare le tasse per l'anno accademico corrente.""",
        "relevant_docs": ["lauree.txt"],
        "category": "laurea"
    },
    {
        "query": "Ho dimenticato il numero di pre-matricola, come lo recupero?",
        "reference_answer": """Per recuperare il numero di pre-matricola consulta la guida: https://www.unibg.it/sites/default/files/how_to_-_recuperare_il_numero_di_pre-matricola.pdf

La guida spiega passo-passo come recuperarlo attraverso il sistema.""",
        "relevant_docs": ["iscrizioni_anno_accademico.txt"],
        "category": "iscrizioni"
    },
    {
        "query": "Dove consegno la tesi di laurea?",
        "reference_answer": """La tesi va consegnata in due modi:

1. **Copia cartacea**: consegna una copia al relatore e all'eventuale correlatore
2. **Copia digitale**: dopo conferma della domanda di laurea dalla Segreteria, carica la tesi in formato PDF nel tuo Sportello Internet entro la scadenza prevista dal Calendario Didattico

La scadenza per il caricamento è riportata sul Calendario Didattico del tuo Dipartimento.""",
        "relevant_docs": ["lauree.txt"],
        "category": "laurea"
    },
    {
        "query": "Quali sono le scadenze per l'iscrizione?",
        "reference_answer": """Le scadenze di iscrizione sono divise tra:
- Lauree triennali (o magistrali a ciclo unico)
- Lauree magistrali

Consulta: https://www.unibg.it/studia-noi/iscriversi/scadenze-iscriversi

ATTENZIONE: per i corsi ad accesso programmato, è essenziale prendere visione dei rispettivi bandi che possono prevedere scadenze diverse.""",
        "relevant_docs": ["iscrizioni_anno_accademico.txt"],
        "category": "iscrizioni"
    },
    {
        "query": "Come calcolo la media del quarto anno necessaria per il bando?",
        "reference_answer": """La media dei voti del 4° anno della scuola superiore deve essere arrotondata alla seconda cifra decimale:
- Se la terza cifra dopo la virgola è ≥5, arrotonda per eccesso
- Esempi: 7,423 → 7,42 mentre 7,425 → 7,43

Devi sempre indicare 2 cifre dopo la virgola: se la media è 8, indica 8,00""",
        "relevant_docs": ["iscrizioni_anno_accademico.txt"],
        "category": "iscrizioni"
    },
    {
        "query": "Posso sostenere il TOLC più volte?",
        "reference_answer": """Sì, puoi sostenere il TOLC più volte.

Per le graduatorie di ammissione ai corsi ad accesso programmato viene considerato il punteggio migliore tra tutti i TOLC sostenuti.

Puoi sostenere il TOLC presso qualsiasi sede universitaria (non solo UniBG). Ricorda di effettuare la pre-iscrizione in UNIBG entro le scadenze previste per far acquisire automaticamente il tuo risultato.""",
        "relevant_docs": ["iscrizioni_anno_accademico.txt"],
        "category": "iscrizioni"
    },
    {
        "query": "Qual è l'offerta formativa dell'Università di Bergamo?",
        "reference_answer": """L'offerta formativa UniBG per l'anno accademico 2024/2025 include corsi di:
- Laurea triennale
- Laurea magistrale
- Laurea magistrale a ciclo unico

Puoi consultare tutti i corsi su:
- https://www.unibg.it/studiare/ti-aiutiamo/scopri-unibg/cerca-tuo-corso-laurea
- https://www.unibg.it/studiare/corsi/offerta-formativa""",
        "relevant_docs": ["iscrizioni_anno_accademico.txt", "guida_dello_studente"],
        "category": "iscrizioni"
    }
]


class ResponseQualityEvaluator:
    """Valutatore qualità risposte ChatBot"""
    
    def __init__(self):
        self.similarity_model = SentenceTransformer('all-MiniLM-L6-v2')
        
    def evaluate_response(self, 
                         question: str,
                         generated_response: str, 
                         reference_response: str = None,
                         context: str = None) -> Dict[str, float]:
        """Valuta qualità risposta con metriche essenziali"""
        
        metrics = {}
        
        metrics.update(self._basic_metrics(generated_response))
        metrics.update(self._relevance_metrics(question, generated_response))
        metrics.update(self._content_quality_metrics(generated_response, context))
        
        if reference_response:
            metrics.update(self._comparative_metrics(generated_response, reference_response))
        
        metrics['overall_score'] = self._calculate_overall_score(metrics)
        
        return metrics
    
    def _basic_metrics(self, response: str) -> Dict[str, float]:
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
        try:
            q_embedding = self.similarity_model.encode([question])
            r_embedding = self.similarity_model.encode([response])
            semantic_sim = cosine_similarity(q_embedding, r_embedding)[0][0]
        except:
            semantic_sim = 0.5
        
        q_words = set(re.findall(r'\w+', question.lower()))
        r_words = set(re.findall(r'\w+', response.lower()))
        keyword_overlap = len(q_words & r_words) / len(q_words) if q_words else 0.0
        
        return {
            'semantic_similarity': float(semantic_sim),
            'keyword_overlap': keyword_overlap
        }
    
    def _content_quality_metrics(self, response: str, context: str = None) -> Dict[str, float]:
        metrics = {
            'completeness_score': self._assess_completeness(response),
            'informativeness_score': self._assess_informativeness(response), 
            'clarity_score': self._assess_clarity(response),
            'professional_tone': self._assess_professional_tone(response)
        }
        
        if context:
            metrics['context_utilization'] = self._assess_context_usage(response, context)
        
        return metrics
    
    def _comparative_metrics(self, generated: str, reference: str) -> Dict[str, float]:
        bleu = self._simple_bleu(generated, reference)
        
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
        score = 0.0
        word_count = len(response.split())
        
        if 30 <= word_count <= 400:
            score += 0.4
        elif word_count >= 15:
            score += 0.2
        
        if any(term in response.lower() for term in ['procedura', 'passo', 'fase', 'primo', 'secondo']):
            score += 0.3
        
        if any(info in response.lower() for info in ['contatto', 'segreteria', 'http', 'email']):
            score += 0.3
        
        return min(score, 1.0)
    
    def _assess_informativeness(self, response: str) -> float:
        score = 0.0
        
        unibg_terms = ['università', 'bergamo', 'unibg', 'segreteria', 'studenti']
        found_terms = sum(1 for term in unibg_terms if term in response.lower())
        score += min(found_terms * 0.1, 0.4)
        
        if re.search(r'\b\d+\b', response):
            score += 0.2
        
        generic_phrases = ['non ho informazioni', 'contatta la segreteria', 'informazioni insufficienti']
        if any(phrase in response.lower() for phrase in generic_phrases):
            score = max(score - 0.3, 0.0)
        else:
            score += 0.4
        
        return min(score, 1.0)
    
    def _assess_clarity(self, response: str) -> float:
        score = 0.0
        sentences = [s.strip() for s in re.split(r'[.!?]+', response) if s.strip()]
        
        if sentences:
            avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences)
            if 8 <= avg_sentence_length <= 25:
                score += 0.4
            elif avg_sentence_length <= 30:
                score += 0.2
        
        if any(marker in response for marker in ['•', '\n-', '1.', '2.']):
            score += 0.3
        
        if any(fmt in response for fmt in ['**', '__', '\n']):
            score += 0.3
        
        return min(score, 1.0)
    
    def _assess_professional_tone(self, response: str) -> float:
        score = 0.7
        
        if any(phrase in response.lower() for phrase in ['gentilmente', 'prego', 'cordiali']):
            score += 0.2
        
        informal_words = ['ciao', 'hey', 'ok', 'boh', 'tipo']
        for word in informal_words:
            if word in response.lower():
                score -= 0.1
        
        return max(min(score, 1.0), 0.0)
    
    def _assess_context_usage(self, response: str, context: str) -> float:
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
        gen_words = generated.lower().split()
        ref_words = reference.lower().split()
        
        if not gen_words or not ref_words:
            return 0.0
        
        gen_counter = Counter(gen_words)
        ref_counter = Counter(ref_words)
        
        overlap = sum((gen_counter & ref_counter).values())
        precision = overlap / len(gen_words) if gen_words else 0.0
        length_penalty = min(1.0, len(gen_words) / len(ref_words)) if ref_words else 0.0
        
        return precision * length_penalty
    
    def _calculate_overall_score(self, metrics: Dict[str, float]) -> float:
        weights = {
            'semantic_similarity': 0.3,
            'completeness_score': 0.2,
            'informativeness_score': 0.2,
            'clarity_score': 0.15,
            'professional_tone': 0.15,
        }
        
        score = 0.0
        total_weight = 0.0
        
        for metric, weight in weights.items():
            if metric in metrics:
                score += metrics[metric] * weight
                total_weight += weight
        
        return round(score / total_weight if total_weight > 0 else 0.0, 3)


class RAGSystemEvaluator:
    """Valutatore specifico per sistemi RAG"""
    
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
        """Valuta sistema RAG con metriche specifiche"""
        
        metrics = {}
        
        if relevant_documents:
            metrics.update(self._calculate_recall_at_k(retrieved_documents, relevant_documents, k_values))
        
        metrics['bleu_score'] = self._calculate_bleu_score(generated_response, reference_response)
        metrics['rouge_l'] = self._calculate_rouge_l(generated_response, reference_response)
        metrics['bert_score'] = self._calculate_bert_score(generated_response, reference_response)
        metrics['answer_relevance'] = self._calculate_answer_relevance(query, generated_response)
        
        if retrieved_documents and relevant_documents:
            metrics['context_precision'] = self._calculate_context_precision(retrieved_documents, relevant_documents)
        
        if retrieved_documents:
            metrics['faithfulness'] = self._calculate_faithfulness(generated_response, retrieved_documents)
        
        metrics['rag_overall_score'] = self._calculate_rag_overall_score(metrics)
        
        return metrics
    
    def _calculate_recall_at_k(self, retrieved_docs: List[str], relevant_docs: List[str], k_values: List[int]) -> Dict[str, float]:
        """
        Calcola Recall@K per diversi valori di K.
        retrieved_docs: contenuto testuale dei documenti recuperati
        relevant_docs: nomi file dei documenti rilevanti
        """
        recall_metrics = {}
        
        # Estrai keywords dai nomi file rilevanti
        relevant_keywords = []
        for doc_name in relevant_docs:
            keyword = doc_name.replace('.txt', '').replace('_', ' ').lower()
            relevant_keywords.append(keyword)
        
        for k in k_values:
            if k <= len(retrieved_docs):
                top_k_retrieved = retrieved_docs[:k]
                
                # Conta quante keywords rilevanti sono presenti nei top-K documenti
                found_keywords = set()
                for doc_content in top_k_retrieved:
                    doc_lower = doc_content.lower()
                    for keyword in relevant_keywords:
                        if keyword in doc_lower:
                            found_keywords.add(keyword)
                
                # Recall = keywords trovate / totale keywords rilevanti
                total_relevant = len(relevant_keywords)
                recall_at_k = len(found_keywords) / total_relevant if total_relevant > 0 else 0.0
                recall_metrics[f'recall_at_{k}'] = round(recall_at_k, 3)
            else:
                recall_metrics[f'recall_at_{k}'] = 0.0
        
        return recall_metrics
    
    def _calculate_bleu_score(self, generated: str, reference: str) -> float:
        if NLTK_AVAILABLE:
            try:
                gen_tokens = generated.lower().split()
                ref_tokens = [reference.lower().split()]
                bleu = sentence_bleu(ref_tokens, gen_tokens, smoothing_function=self.smoothing_function)
                return round(bleu, 3)
            except:
                pass
        
        return self._simple_bleu_fallback(generated, reference)
    
    def _calculate_rouge_l(self, generated: str, reference: str) -> float:
        if ROUGE_AVAILABLE:
            try:
                scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
                scores = scorer.score(reference, generated)
                return round(scores['rougeL'].fmeasure, 3)
            except:
                pass
        
        return self._simple_rouge_l_fallback(generated, reference)
    
    def _calculate_bert_score(self, generated: str, reference: str) -> float:
        try:
            gen_embedding = self.similarity_model.encode([generated])
            ref_embedding = self.similarity_model.encode([reference])
            bert_score = cosine_similarity(gen_embedding, ref_embedding)[0][0]
            return round(float(bert_score), 3)
        except:
            return 0.5
    
    def _calculate_answer_relevance(self, query: str, answer: str) -> float:
        try:
            query_embedding = self.similarity_model.encode([query])
            answer_embedding = self.similarity_model.encode([answer])
            relevance = cosine_similarity(query_embedding, answer_embedding)[0][0]
            return round(float(relevance), 3)
        except:
            return 0.5
    
    def _calculate_context_precision(self, retrieved_docs: List[str], relevant_docs: List[str]) -> float:
        """
        Calcola precisione contestuale confrontando documenti recuperati con quelli rilevanti.
        Nota: retrieved_docs contiene il contenuto testuale, relevant_docs contiene nomi file.
        Confronto semantico basato su keyword matching.
        """
        if not retrieved_docs or not relevant_docs:
            return 0.0
        
        # Estrai keywords dai nomi file rilevanti (es: "tasse.txt" -> "tasse")
        relevant_keywords = []
        for doc_name in relevant_docs:
            # Rimuovi estensione e converti in lowercase
            keyword = doc_name.replace('.txt', '').replace('_', ' ').lower()
            relevant_keywords.append(keyword)
        
        # Verifica quanti documenti recuperati contengono le keywords rilevanti
        relevant_retrieved = 0
        for doc_content in retrieved_docs:
            doc_lower = doc_content.lower()
            # Se il contenuto contiene una delle keywords rilevanti
            if any(keyword in doc_lower for keyword in relevant_keywords):
                relevant_retrieved += 1
        
        precision = relevant_retrieved / len(retrieved_docs)
        
        return round(precision, 3)
    
    def _calculate_faithfulness(self, response: str, context_docs: List[str]) -> float:
        if not context_docs:
            return 0.0
        
        try:
            full_context = " ".join(context_docs)
            response_embedding = self.similarity_model.encode([response])
            context_embedding = self.similarity_model.encode([full_context])
            faithfulness = cosine_similarity(response_embedding, context_embedding)[0][0]
            return round(float(faithfulness), 3)
        except:
            return 0.5
    
    def _simple_bleu_fallback(self, generated: str, reference: str) -> float:
        gen_words = generated.lower().split()
        ref_words = reference.lower().split()
        
        if not gen_words or not ref_words:
            return 0.0
        
        gen_1grams = Counter(gen_words)
        ref_1grams = Counter(ref_words)
        gen_2grams = Counter(zip(gen_words[:-1], gen_words[1:]))
        ref_2grams = Counter(zip(ref_words[:-1], ref_words[1:]))
        
        overlap_1 = sum((gen_1grams & ref_1grams).values())
        precision_1 = overlap_1 / len(gen_words) if gen_words else 0.0
        
        overlap_2 = sum((gen_2grams & ref_2grams).values())
        precision_2 = overlap_2 / max(len(gen_words) - 1, 1) if len(gen_words) > 1 else 0.0
        
        avg_precision = (precision_1 + precision_2) / 2
        bp = min(1.0, len(gen_words) / len(ref_words)) if ref_words else 0.0
        
        return round(avg_precision * bp, 3)
    
    def _simple_rouge_l_fallback(self, generated: str, reference: str) -> float:
        gen_words = generated.lower().split()
        ref_words = reference.lower().split()
        
        if not gen_words or not ref_words:
            return 0.0
        
        lcs_length = self._lcs_length(gen_words, ref_words)
        
        precision = lcs_length / len(gen_words) if gen_words else 0.0
        recall = lcs_length / len(ref_words) if ref_words else 0.0
        
        if precision + recall == 0:
            return 0.0
        
        f1 = (2 * precision * recall) / (precision + recall)
        return round(f1, 3)
    
    def _lcs_length(self, seq1: List[str], seq2: List[str]) -> int:
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
        rag_weights = {
            'bleu_score': 0.2,
            'rouge_l': 0.15,
            'bert_score': 0.25,
            'answer_relevance': 0.2,
            'context_precision': 0.1,
            'faithfulness': 0.1,
        }
        
        score = 0.0
        total_weight = 0.0
        
        for metric, weight in rag_weights.items():
            if metric in metrics:
                score += metrics[metric] * weight
                total_weight += weight
        
        recall_keys = [k for k in metrics.keys() if k.startswith('recall_at_')]
        if recall_keys:
            avg_recall = sum(metrics[k] for k in recall_keys) / len(recall_keys)
            score += avg_recall * 0.1
            total_weight += 0.1
        
        return round(score / total_weight if total_weight > 0 else 0.0, 3)

def evaluate_rag_with_real_chatbot(query: str, chatbot, reference_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Valuta risposta del chatbot reale con ground truth dal dataset
    """
    
    # Recupera i documenti effettivamente utilizzati dal RAG
    retrieved_docs_objs = chatbot.retrieve_documents(query, k=5)
    retrieved_docs_content = [doc['content'] for doc in retrieved_docs_objs] if retrieved_docs_objs else []
    
    # Genera risposta del chatbot
    chatbot_response = chatbot.chat(query)
    generated_response = chatbot_response['response']
    
    # Documenti rilevanti di riferimento (per confronto)
    relevant_docs = reference_data.get('relevant_docs', [])
    
    quality_evaluator = ResponseQualityEvaluator()
    quality_metrics = quality_evaluator.evaluate_response(
        query, 
        generated_response, 
        reference_data['reference_answer']
    )
    
    rag_evaluator = RAGSystemEvaluator()
    rag_metrics = rag_evaluator.evaluate_rag_system(
        query=query,
        generated_response=generated_response,
        reference_response=reference_data['reference_answer'],
        retrieved_documents=retrieved_docs_content,
        relevant_documents=relevant_docs
    )
    
    result = {
        'query': query,
        'category': reference_data.get('category', 'unknown'),
        'generated_response': generated_response,
        'reference_response': reference_data['reference_answer'],
        'retrieved_documents': [doc[:200] + "..." for doc in retrieved_docs_content[:3]],  # Primi 3 docs troncati
        'num_retrieved_docs': len(retrieved_docs_content),
        'quality_metrics': quality_metrics,
        'rag_metrics': rag_metrics,
        'overall_quality_score': quality_metrics['overall_score'],
        'overall_rag_score': rag_metrics['rag_overall_score']
    }
    
    return result


def batch_evaluate_rag_system(num_samples: int = 5, save_results: bool = True) -> Dict[str, Any]:
    """
    Valuta il sistema RAG su N campioni casuali dal dataset
    """
    
    # Assicurati di essere nella directory corretta (root del progetto)
    script_dir = Path(__file__).parent.parent
    os.chdir(script_dir)
    
    sys.path.append(str(script_dir))
    try:
        from main import ChatbotRAG
        chatbot = ChatbotRAG()
    except Exception as e:
        print(f"Errore importazione chatbot: {e}")
        print("Assicurati che main.py sia accessibile e l'ambiente virtuale sia attivo")
        return {}
    
    import random
    samples = random.sample(REFERENCE_DATASET, min(num_samples, len(REFERENCE_DATASET)))
    
    results = []
    print(f"\n{'='*80}")
    print(f"VALUTAZIONE BATCH SISTEMA RAG - {num_samples} campioni")
    print(f"{'='*80}\n")
    
    for idx, sample in enumerate(samples, 1):
        print(f"[{idx}/{num_samples}] Valutando: {sample['query'][:60]}...")
        
        try:
            result = evaluate_rag_with_real_chatbot(
                query=sample['query'],
                chatbot=chatbot,
                reference_data=sample
            )
            results.append(result)
            
            print(f"  Quality Score: {result['overall_quality_score']:.3f}")
            print(f"  RAG Score: {result['overall_rag_score']:.3f}\n")
            
        except Exception as e:
            print(f"  Errore: {e}\n")
            continue
    
    if results:
        quality_scores = [r['overall_quality_score'] for r in results]
        rag_scores = [r['overall_rag_score'] for r in results]
        bleu_scores = [r['rag_metrics']['bleu_score'] for r in results]
        rouge_scores = [r['rag_metrics']['rouge_l'] for r in results]
        bert_scores = [r['rag_metrics']['bert_score'] for r in results]
        
        aggregate_stats = {
            'num_samples': len(results),
            'quality_score': {
                'mean': round(np.mean(quality_scores), 3),
                'std': round(np.std(quality_scores), 3),
                'min': round(np.min(quality_scores), 3),
                'max': round(np.max(quality_scores), 3)
            },
            'rag_score': {
                'mean': round(np.mean(rag_scores), 3),
                'std': round(np.std(rag_scores), 3),
                'min': round(np.min(rag_scores), 3),
                'max': round(np.max(rag_scores), 3)
            },
            'bleu': {'mean': round(np.mean(bleu_scores), 3), 'std': round(np.std(bleu_scores), 3)},
            'rouge_l': {'mean': round(np.mean(rouge_scores), 3), 'std': round(np.std(rouge_scores), 3)},
            'bert_score': {'mean': round(np.mean(bert_scores), 3), 'std': round(np.std(bert_scores), 3)}
        }
        
        best_idx = quality_scores.index(max(quality_scores))
        worst_idx = quality_scores.index(min(quality_scores))
        
        batch_result = {
            'timestamp': __import__('time').strftime('%Y-%m-%d %H:%M:%S'),
            'analysis_type': 'Batch RAG Evaluation',
            'dataset_size': len(REFERENCE_DATASET),
            'samples_evaluated': len(results),
            'aggregate_statistics': aggregate_stats,
            'best_case': {
                'query': results[best_idx]['query'],
                'quality_score': results[best_idx]['overall_quality_score'],
                'rag_score': results[best_idx]['overall_rag_score']
            },
            'worst_case': {
                'query': results[worst_idx]['query'],
                'quality_score': results[worst_idx]['overall_quality_score'],
                'rag_score': results[worst_idx]['overall_rag_score']
            },
            'detailed_results': results
        }
        
        if save_results:
            results_dir = Path(__file__).parent.parent / 'results'
            results_dir.mkdir(exist_ok=True)
            
            output_file = results_dir / 'metriche_rag_results.json'
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(batch_result, f, indent=2, ensure_ascii=False)
            
            print(f"\n{'='*80}")
            print(f"RISULTATI SALVATI: {output_file}")
            print(f"{'='*80}\n")
            
            print("STATISTICHE AGGREGATE:")
            print(f"  Quality Score: {aggregate_stats['quality_score']['mean']:.3f} ± {aggregate_stats['quality_score']['std']:.3f}")
            print(f"  RAG Score: {aggregate_stats['rag_score']['mean']:.3f} ± {aggregate_stats['rag_score']['std']:.3f}")
            print(f"  BLEU: {aggregate_stats['bleu']['mean']:.3f}")
            print(f"  ROUGE-L: {aggregate_stats['rouge_l']['mean']:.3f}")
            print(f"  BERT Score: {aggregate_stats['bert_score']['mean']:.3f}\n")
        
        return batch_result
    
    return {}


def test_single_rag_evaluation():
    """Test singola valutazione RAG"""
    print("\n" + "="*80)
    print("TEST SINGOLA VALUTAZIONE RAG")
    print("="*80 + "\n")
    
    # Assicurati di essere nella directory corretta (root del progetto)
    script_dir = Path(__file__).parent.parent
    os.chdir(script_dir)
    
    sys.path.append(str(script_dir))
    try:
        from main import ChatbotRAG
        chatbot = ChatbotRAG()
    except Exception as e:
        print(f"Errore: impossibile importare chatbot. {e}")
        return
    
    sample = REFERENCE_DATASET[0]
    
    print(f"Query: {sample['query']}\n")
    
    result = evaluate_rag_with_real_chatbot(
        query=sample['query'],
        chatbot=chatbot,
        reference_data=sample
    )
    
    print(f"Risposta generata: {result['generated_response'][:200]}...\n")
    print(f"Overall Quality Score: {result['overall_quality_score']}")
    print(f"Overall RAG Score: {result['overall_rag_score']}")
    print(f"\nMetriche RAG:")
    print(f"  BLEU: {result['rag_metrics']['bleu_score']}")
    print(f"  ROUGE-L: {result['rag_metrics']['rouge_l']}")
    print(f"  BERT Score: {result['rag_metrics']['bert_score']}")
    print(f"  Answer Relevance: {result['rag_metrics']['answer_relevance']}")
    
    results_dir = Path(__file__).parent.parent / 'results'
    results_dir.mkdir(exist_ok=True)
    
    output_file = results_dir / 'metriche_rag_results.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"\nRisultati salvati in: {output_file}")


def test_batch_rag_evaluation():
    """Test valutazione batch su 5 campioni"""
    batch_evaluate_rag_system(num_samples=5, save_results=True)


if __name__ == "__main__":
    print("\n" + "="*80)
    print("SISTEMA VALUTAZIONE RAG - CHATBOT UNIBG")
    print("="*80)
    print(f"\nDataset di riferimento: {len(REFERENCE_DATASET)} coppie domanda-risposta")
    print("Categorie: iscrizioni, tasse, esami, laurea, certificati, servizi")
    print("\nScegli un'opzione:")
    print("  1. Test singola valutazione")
    print("  2. Test batch (5 campioni casuali)")
    print("  3. Entrambi")
    
    try:
        choice = input("\nOpzione (1/2/3): ").strip()
        
        if choice == '1':
            test_single_rag_evaluation()
        elif choice == '2':
            test_batch_rag_evaluation()
        elif choice == '3':
            test_single_rag_evaluation()
            print("\n")
            test_batch_rag_evaluation()
        else:
            print("Opzione non valida. Eseguo test singolo...")
            test_single_rag_evaluation()
            
    except KeyboardInterrupt:
        print("\n\nInterrotto dall'utente.")
    except Exception as e:
        print(f"\n\nErrore: {e}")
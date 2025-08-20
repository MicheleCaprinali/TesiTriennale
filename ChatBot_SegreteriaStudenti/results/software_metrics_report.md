# REPORT METRICHE SOFTWARE - ChatBot RAG

## SUMMARY GENERALE

- **File analizzati:** 17
- **Linee di codice totali:** 2625
- **Classi totali:** 6
- **Funzioni totali:** 79
- **Import totali:** 91
- **CC medio:** 2.96
- **CC massimo:** 14

## ANALISI PER FILE

### main.py
- **LOC:** 214
- **Classi:** 0
- **Funzioni:** 6
- **CC totale:** 36

### setup.py
- **LOC:** 305
- **Classi:** 0
- **Funzioni:** 11
- **CC totale:** 51

### software_metrics.py
- **LOC:** 421
- **Classi:** 1
- **Funzioni:** 13
- **CC totale:** 66
  - **Classe CodeMetricsAnalyzer:** WMC=63, LCOM=0.97

### thesis_evaluation.py
- **LOC:** 217
- **Classi:** 1
- **Funzioni:** 7
- **CC totale:** 23
  - **Classe ThesisEvaluator:** WMC=23, LCOM=0.86

### streamlit_app.py
- **LOC:** 250
- **Classi:** 0
- **Funzioni:** 3
- **CC totale:** 20

### analytics.py
- **LOC:** 180
- **Classi:** 1
- **Funzioni:** 9
- **CC totale:** 15
  - **Classe ChatbotAnalytics:** WMC=9, LCOM=0.00

### chatbot.py
- **LOC:** 245
- **Classi:** 1
- **Funzioni:** 7
- **CC totale:** 39
  - **Classe ChatbotRAG:** WMC=35, LCOM=0.87

### create_vectorstore.py
- **LOC:** 110
- **Classi:** 0
- **Funzioni:** 2
- **CC totale:** 6

### extract_and_save.py
- **LOC:** 49
- **Classi:** 0
- **Funzioni:** 1
- **CC totale:** 7

### extract_file.py
- **LOC:** 28
- **Classi:** 0
- **Funzioni:** 1
- **CC totale:** 5

### local_embeddings.py
- **LOC:** 44
- **Classi:** 1
- **Funzioni:** 3
- **CC totale:** 4
  - **Classe LocalEmbeddings:** WMC=4, LCOM=0.00

### ollama_llm.py
- **LOC:** 177
- **Classi:** 1
- **Funzioni:** 6
- **CC totale:** 25
  - **Classe OllamaLLM:** WMC=21, LCOM=0.00

### split_into_chunks.py
- **LOC:** 47
- **Classi:** 0
- **Funzioni:** 2
- **CC totale:** 3

### __init__.py
- **LOC:** 1
- **Classi:** 0
- **Funzioni:** 0
- **CC totale:** 0

### generate_test_data.py
- **LOC:** 153
- **Classi:** 0
- **Funzioni:** 4
- **CC totale:** 21

### test_links.py
- **LOC:** 58
- **Classi:** 0
- **Funzioni:** 1
- **CC totale:** 6

### test_retrieval.py
- **LOC:** 126
- **Classi:** 0
- **Funzioni:** 3
- **CC totale:** 22

## METRICHE ROBERT MARTIN

| Modulo | Ca (Afferent) | Ce (Efferent) | Instability |
|--------|---------------|---------------|-------------|
| main | 0 | 10 | 1.000 |
| setup | 1 | 8 | 0.889 |
| software_metrics | 0 | 9 | 1.000 |
| thesis_evaluation | 0 | 11 | 1.000 |
| streamlit_app | 0 | 7 | 1.000 |
| analytics | 0 | 5 | 1.000 |
| chatbot | 5 | 6 | 0.545 |
| create_vectorstore | 3 | 7 | 0.700 |
| extract_and_save | 1 | 2 | 0.667 |
| extract_file | 1 | 2 | 0.667 |
| local_embeddings | 3 | 4 | 0.571 |
| ollama_llm | 2 | 6 | 0.750 |
| split_into_chunks | 1 | 2 | 0.667 |
| __init__ | 0 | 0 | 0.000 |
| generate_test_data | 0 | 4 | 1.000 |
| test_links | 0 | 4 | 1.000 |
| test_retrieval | 0 | 4 | 1.000 |

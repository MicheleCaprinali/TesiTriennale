# REPORT METRICHE SOFTWARE - ChatBot 

## RIASSUNTO GENERALE

- **File analizzati:** 13
- **Classi totali:** 4
- **Funzioni totali:** 31
- **Import totali:** 66
- **CC medio:** 2.81
- **CC massimo:** 14

## ANALISI PER FILE

### main.py
- **LOC:** 230
- **Classi:** 0
- **Funzioni:** 6
- **CC totale:** 36

### setup.py
- **LOC:** 321
- **Classi:** 0
- **Funzioni:** 11
- **CC totale:** 51

### thesis_evaluation.py
- **LOC:** 223
- **Classi:** 1
- **Funzioni:** 0
- **CC totale:** 0
  - **Classe ThesisEvaluator:** WMC=23, LCOM=0.86

### analytics.py
- **LOC:** 210
- **Classi:** 1
- **Funzioni:** 3
- **CC totale:** 6
  - **Classe ChatbotAnalytics:** WMC=9, LCOM=0.00

### create_vectorstore.py
- **LOC:** 135
- **Classi:** 0
- **Funzioni:** 2
- **CC totale:** 6

### extract_and_save.py
- **LOC:** 49
- **Classi:** 0
- **Funzioni:** 1
- **CC totale:** 7

### extract_file.py
- **LOC:** 35
- **Classi:** 0
- **Funzioni:** 1
- **CC totale:** 5

### local_embeddings.py
- **LOC:** 52
- **Classi:** 1
- **Funzioni:** 0
- **CC totale:** 0
  - **Classe LocalEmbeddings:** WMC=4, LCOM=0.00

### ollama_llm.py
- **LOC:** 185
- **Classi:** 1
- **Funzioni:** 1
- **CC totale:** 4
  - **Classe OllamaLLM:** WMC=21, LCOM=0.00

### split_into_chunks.py
- **LOC:** 60
- **Classi:** 0
- **Funzioni:** 2
- **CC totale:** 3

### __init__.py
- **LOC:** 1
- **Classi:** 0
- **Funzioni:** 0
- **CC totale:** 0

### test_links.py
- **LOC:** 58
- **Classi:** 0
- **Funzioni:** 1
- **CC totale:** 6

### test_retrieval.py
- **LOC:** 128
- **Classi:** 0
- **Funzioni:** 3
- **CC totale:** 22

## METRICHE ROBERT MARTIN

| Modulo | Ca (Afferent) | Ce (Efferent) | Instability |
|--------|---------------|---------------|-------------|
| main | 0 | 10 | 1.000 |
| setup | 1 | 8 | 0.889 |
| thesis_evaluation | 0 | 11 | 1.000 |
| analytics | 0 | 6 | 1.000 |
| create_vectorstore | 2 | 7 | 0.778 |
| extract_and_save | 1 | 2 | 0.667 |
| extract_file | 1 | 2 | 0.667 |
| local_embeddings | 2 | 4 | 0.667 |
| ollama_llm | 1 | 6 | 0.857 |
| split_into_chunks | 1 | 2 | 0.667 |
| __init__ | 0 | 0 | 0.000 |
| test_links | 0 | 4 | 1.000 |
| test_retrieval | 0 | 4 | 1.000 |

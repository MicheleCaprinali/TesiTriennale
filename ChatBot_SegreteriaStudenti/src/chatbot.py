from dotenv import load_dotenv
load_dotenv()  # Carica le variabili d'ambiente dal file .env

import os
from langchain.embeddings import OpenAIEmbeddings
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI
from langchain_openai import OpenAI
from langchain.chains import RetrievalQA

# Carica il vectorstore creato in precedenza
def load_vectorstore(persist_dir="vectordb"):
    embeddings = OpenAIEmbeddings()
    vectordb = Chroma(persist_directory=persist_dir, embedding_function=embeddings)
    return vectordb

def crea_chatbot():
    vectordb = load_vectorstore()
    llm = OpenAI(temperature=0)  # puoi mettere GPT-4 se hai accesso
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=vectordb.as_retriever())
    return qa_chain

if __name__ == "__main__":
    print("🎓 ChatBot Segreteria Studenti")
    print("Scrivi una domanda o 'exit' per uscire\n")

    chatbot = crea_chatbot()

    while True:
        domanda = input("Studente 👤 > ")
        if domanda.lower() in ["exit", "quit"]:
            break
        risposta = chatbot.run(domanda)

        # Verifica se la risposta è vaga o non pertinente
        if "non sono sicuro" in risposta.lower() or len(risposta.strip()) < 20:
            print("🤖 > Non sono sicuro. Ti consiglio di aprire un ticket alla Segreteria.")
        else:
            print(f"🤖 > {risposta}\n")

import sys
import os
import streamlit as st
from task_1_pdf_processor import DocumentProcessor
from task_2_embedding import EmbeddingClient
from task_3_chromaDB import ChromaCollectionCreator

if __name__ == "__main__":
    st.header("Quizzify")

    # Configuration for EmbeddingClient
    embed_config = {
        "model_name": "textembedding-gecko@003",
        "project": "Enter your project ID here",
        "location": "your location"
    }
    
    screen = st.empty() # Screen 1, ingest documents
    with screen.container():
        st.header("Quizzify")
        processor = DocumentProcessor()
        processor.ingest_documents()
        embed_client = EmbeddingClient(embed_config['model_name'],embed_config['project'],embed_config['location'])
        chroma_creator = ChromaCollectionCreator(processor, embed_client)
        with st.form("Load Data to Chroma"):
            st.subheader("Quiz Builder")
            st.write("Select PDFs for Ingestion, the topic for the quiz, and click Generate!")
            topic_input = st.text_input("Enter Quiz Topic: ")
            num_questions = st.number_input("Enter number of questions:", min_value=1, step=1, value=5)
            document = None
            
            submitted = st.form_submit_button("Generate a Quiz!")
            if submitted:
                # Use the create_chroma_collection() method to create a Chroma collection from the processed documents
                chroma_creator.create_chroma_collection()
                document = chroma_creator.query_chroma_collection(topic_input) 
                
    if document:
        screen.empty() # Screen 2
        with st.container():
            st.header("Query Chroma for Topic, top Document: ")
            st.write(document)

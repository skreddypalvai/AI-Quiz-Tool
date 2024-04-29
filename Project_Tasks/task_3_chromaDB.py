import sys
import os
import streamlit as st
from task_1_pdf_processor import DocumentProcessor
from task_2_embedding import EmbeddingClient
# Import Task libraries
from langchain_core.documents import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma

class ChromaCollectionCreator:
    def __init__(self, processor, embed_model):

        self.processor = processor      # This will hold the DocumentProcessor from step 3
        self.embed_model = embed_model  # This will hold the EmbeddingClient from step 4
        self.db = None                  # This will hold the Chroma collection
    
    def create_chroma_collection(self):

        
        # Check for processed documents
        if len(self.processor.pages) == 0:
            st.error("No documents found!", icon="🚨")
            return

        text_splitter = CharacterTextSplitter(separator="\n\n",chunk_size=1000,chunk_overlap=200,length_function=len,
                                              is_separator_regex=False)
        texts = [doc.page_content for doc in self.processor.pages]
        #processed_pages = [str(page) for page in self.processor.pages]
        texts = text_splitter.create_documents(texts)
        if texts is not None:
            st.success(f"Successfully split pages to {len(texts)} documents!", icon="✅")


        self.db = Chroma.from_documents(texts, self.embed_model)
        if self.db:
            st.success("Successfully created Chroma Collection!", icon="✅")
        else:
            st.error("Failed to create Chroma Collection!", icon="🚨")
    
    def query_chroma_collection(self, query) -> Document:

        if self.db:
            docs = self.db.similarity_search_with_relevance_scores(query)
            if docs:
                return docs[0]
            else:
                st.error("No matching documents found!", icon="🚨")
        else:
            st.error("Chroma Collection has not been created!", icon="🚨")
    def as_retriever(self):
        return self.db.as_retriever()


if __name__ == "__main__":
    processor = DocumentProcessor() # Initialize from step 3
    processor.ingest_documents()
    
    embed_config = {
        "model_name": "textembedding-gecko@003",
        "project": "my-quiz-project-420005",
        "location": "us-central1"
    }
    
    embed_client = EmbeddingClient(**embed_config) # Initialize from step 4
   
    chroma_creator = ChromaCollectionCreator(processor, embed_client)   
    with st.form("Load Data to Chroma"):
        st.write("Select PDFs for Ingestion, then click Submit")
        
        submitted = st.form_submit_button("Submit")
        if submitted:
            chroma_creator.create_chroma_collection()
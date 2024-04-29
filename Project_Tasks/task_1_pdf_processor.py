# pdf_processing.py

# Necessary imports
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
import os
import tempfile
import uuid

class DocumentProcessor:

    def __init__(self):
        self.pages = []  # List to keep track of pages from all documents
    
    def ingest_documents(self):

        # Render a file uploader widget.
        uploaded_files = st.file_uploader("Upload PDF Files",type="pdf",accept_multiple_files=True)
        
        if uploaded_files is not None:
            for uploaded_file in uploaded_files:
                # Generate a unique identifier to append to the file's original name
                unique_id = uuid.uuid4().hex
                original_name, file_extension = os.path.splitext(uploaded_file.name)
                temp_file_name = f"{original_name}_{unique_id}{file_extension}"
                temp_file_path = os.path.join(tempfile.gettempdir(), temp_file_name)

                # Write the uploaded PDF to a temporary file
                with open(temp_file_path, 'wb') as f:
                    f.write(uploaded_file.getvalue())
                
                # Process the temporary file
                try:
                    pdf_loader = PyPDFLoader(temp_file_path)
                    pdf_docs = pdf_loader.load()
                    for pdf_doc in pdf_docs:        
                        self.pages.append(pdf_doc)
                            #print("Page added:", page)
                except Exception as e:
                    st.error(f"Error processing {uploaded_file.name}: {str(e)}")
                
                # Clean up by deleting the temporary file.
                os.unlink(temp_file_path)
            
            # Display the total number of pages processed.
            st.write(f"Total pages processed: {len(self.pages)}")
        
if __name__ == "__main__":
    processor = DocumentProcessor()
    processor.ingest_documents()
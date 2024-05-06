import streamlit as st
import os
import sys
import json
from task_1_pdf_processor import DocumentProcessor
from task_2_embedding import EmbeddingClient
from task_3_chromaDB import ChromaCollectionCreator
from task_6_validatequiz import QuizGenerator

class QuizManager:

    def __init__(self, questions: list):
        self.questions= questions
        self.total_questions = len(self.questions)

    def get_question_at_index(self, index: int):
        # Ensure index is always within bounds using modulo arithmetic
        valid_index = index % self.total_questions
        return self.questions[valid_index]

    def next_question_index(self, direction=1):
        if st.session_state['question_index'] is not None:
            current_idx = st.session_state.get("question_index",0)
            new_index = (current_idx+direction)% self.total_questions
            st.session_state['question_index'] = new_index
        else:
            raise ValueError("session_state not found")  

# Test Generating the Quiz
if __name__ == "__main__":
    
    embed_config = {
        "model_name": "textembedding-gecko@003",
        "project": "Enter your project ID here",
        "location": "your location"
    }
    
    screen = st.empty()
    with screen.container():
        st.header("Quiz Builder")
        processor = DocumentProcessor()
        processor.ingest_documents()
    
        embed_client = EmbeddingClient(**embed_config) 
    
        chroma_creator = ChromaCollectionCreator(processor, embed_client)
    
        question = None
        question_bank = None
    
        with st.form("Load Data to Chroma"):
            st.subheader("Quiz Builder")
            st.write("Select PDFs for Ingestion, the topic for the quiz, and click Generate!")
            
            topic_input = st.text_input("Topic for Generative Quiz", placeholder="Enter the topic of the document")
            questions = st.slider("Number of Questions", min_value=1, max_value=10, value=1)
            
            submitted = st.form_submit_button("Submit")
            if submitted:
                chroma_creator.create_chroma_collection()
                
                st.write(topic_input)
                
                # Test the Quiz Generator
                generator = QuizGenerator(topic_input, questions, chroma_creator)
                question_bank = generator.generate_quiz()

    if question_bank:
        screen.empty()
        with st.container():
            st.header("Generated Quiz Question: ")

            quiz_manager = QuizManager(question_bank) # Use our new QuizManager class
            # Format the question and display
            with st.form("Multiple Choice Question"):
                index_question = quiz_manager.get_question_at_index(0)# Use the get_question_at_index method to set the 0th index
                
                # Unpack choices for radio
                choices = []
                for choice in index_question['choices']: # For loop unpack the data structure
                    key = choice['key']
                    value = choice['value']
                    choices.append(f"{key}) {value}")

                st.write(f"{index_question['question']}")

                answer = st.radio( # Display the radio button with the choices
                    'Choose the correct answer',
                    choices
                )
                st.form_submit_button("Submit")
                
                if submitted: # On click submit 
                    correct_answer_key = index_question['answer']
                    if answer.startswith(correct_answer_key): # Check if answer is correct
                        st.success("Correct!")
                    else:
                        st.error("Incorrect!")

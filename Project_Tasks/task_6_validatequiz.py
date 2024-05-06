import streamlit as st
import os
import sys
import json
from task_1_pdf_processor import DocumentProcessor
from task_2_embedding import EmbeddingClient
from task_3_chromaDB import ChromaCollectionCreator
from langchain_core.prompts import PromptTemplate
from langchain_google_vertexai import VertexAI
class QuizGenerator:
    def __init__(self, topic=None, num_questions=1, vectorstore=None):
        if not topic:
            self.topic = "General Knowledge"
        else:
            self.topic = topic

        if num_questions > 10:
            raise ValueError("Number of questions cannot exceed 10.")
        self.num_questions = num_questions

        self.vectorstore = vectorstore
        self.llm = None
        self.question_bank = [] # Initialize the question bank to store questions
        self.system_template = """
            You are a subject matter expert on the topic: {topic}
            
            Follow the instructions to create a quiz question:
            1. Generate a question based on the topic provided and context as key "question"
            2. Provide 4 multiple choice answers to the question as a list of key-value pairs "choices"
            3. Provide the correct answer for the question from the list of answers as key "answer"
            4. Provide an explanation as to why the answer is correct as key "explanation"
            
            *You must respond as following structure, Do NOT make it in JSON markdown format:*
                "question": "<question>",
                "choices": [
                    {{"key": "A", "value": "<choice>"}},
                    {{"key": "B", "value": "<choice>"}},
                    {{"key": "C", "value": "<choice>"}},
                    {{"key": "D", "value": "<choice>"}}
                ],
                "answer": "<answer key from choices list>",
                "explanation": "<explanation as to why the answer is correct>"
            }}
            
            Context: {context}
            """
    
    def init_llm(self):
        self.llm = VertexAI(
            model_name = "gemini-pro",
            temperature = 0.8, # Increased for less deterministic questions 
            max_output_tokens = 500
        )

    def generate_question_with_vectorstore(self):
        if not self.llm:
            self.init_llm()
        if not self.vectorstore:
            raise ValueError("Vectorstore not provided.")
        
        from langchain_core.runnables import RunnablePassthrough, RunnableParallel

        # Enable a Retriever
        retriever = self.vectorstore.as_retriever()
        
        # Use the system template to create a PromptTemplate
        prompt = PromptTemplate.from_template(self.system_template)
        
        # RunnableParallel allows Retriever to get relevant documents
        # RunnablePassthrough allows chain.invoke to send self.topic to LLM
        setup_and_retrieval = RunnableParallel(
            {"context": retriever, "topic": RunnablePassthrough()}
        )
        # Create a chain with the Retriever, PromptTemplate, and LLM
        chain = setup_and_retrieval | prompt | self.llm 

        # Invoke the chain with the topic as input
        response = chain.invoke(self.topic)
        return response

    def generate_quiz(self) -> list:
        self.question_bank = [] # Reset the question bank
        #uniq_questions = []
        retry_limit = 3
        max_retries = retry_limit*self.num_questions
        for _ in range(self.num_questions):
            retry_count = 0
            while retry_count<retry_limit:
              question_str = self.generate_question_with_vectorstore()
              question_str = question_str.replace("```json", "").replace("```", "")
              print(question_str)
              try:
                question = json.loads(question_str)
                if self.validate_question(question):
                    print("Successfully generated unique question")
                    self.question_bank.append(question)
                    break
                else:
                    print("Duplicate question detected")
              except json.JSONDecodeError:
                print("Failed to decode question JSON.")
                retry_count +=1
                if retry_count >= max_retries:
                    print("Maximum retries reached.") # Skip this iteration if JSON decoding fails
                    break
            # Validate the question using the validate_question method
            if self.validate_question(question):
                print("Successfully generated unique question")
                self.question_bank.append(question)
            else:
                print("Duplicate or invalid question detected.")
                retry_count += 1
                if retry_count >= max_retries:
                    print("Maximum retries reached.")
                    break

        return self.question_bank
    #def validate_question(self, question: dict) -> bool:
    # Remove markdown tags "```json" and "```" from the question text
     #   question_text = question['question'].replace("```json", "").replace("```", "")
    # Compare the modified question text with existing questions in the question_bank
      #  for existing_question in self.question_bank:
       #     if existing_question_text == question_text:
        #        return False
        #return True
    def validate_question(self, question: dict) -> bool:
        is_unique = True
        question_text = question['question']
        if question_text is None:
            is_unique = False
        for existing_question in self.question_bank:
            if existing_question['question'] == question_text:
                is_unique = False
        return is_unique


# Test Generating the Quiz
if __name__ == "__main__":
    
    embed_config = {
        "model_name": "textembedding-gecko@003",
        "project": "Enter your project ID here",
        "location": "your location"
    }
    
    screen = st.empty()
    with screen.container():
        st.header("Saikiran's AI Quiz Tool")
        processor = DocumentProcessor()
        processor.ingest_documents()
    
        embed_client = EmbeddingClient(**embed_config) # Initialize from step 4
    
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
                question = question_bank[0]

    if question_bank:
        screen.empty()
        with st.container():
            st.header("Generated Quiz Question: ")
            for question in question_bank:
                st.write(question)

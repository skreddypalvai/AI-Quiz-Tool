# Quizzify: AI Quiz Generative Tool
## About:
Quizzify is an AI Quiz tool which is powered by large language model (Google – GEMINI). It focuses on providing individuals especially students with accessible and effective means to reinforce their understanding of various topics. Utilizing cutting edge AI methodologies, the tool dynamically generates quizzes based on user provided documents, facilitated by LangChain for document processing and connecting to LLM. It further enhances the learning experience through the integration of Vertex AI for embeddings and the GEMINI large language model. ChromaDB serves as the repository for storing these embeddings, ensuring efficient data management. Moreover, Quizzify leverages Streamlit for its user interfaces, providing an intuitive and interactive platform for users to engage with generated quizzes.
## Initial Setup:
* To use Vertex AI services, you need to sign in to Google Cloud and navigate to the console to initiate a new project. Then, enable the recommended API in Vertex AI service and you can explore the pretrained models in the model garden. The next step is to select IAM & Admin, choose the service account, and create a new service account where you can access the authentication keys for your Google Cloud services. When creating the service accounts, ensure to select the basic role with owner as a subrole in the service account filter. After creating the service account, navigate to the key section and select "Add key" with JSON format.

  Next, you need to install the gcloud CLI (Command Line Interface). After downloading, run necessary commands in the GCloud SDK Shell, which includes initializing the SDK.
  ```sh
  gcloud init
  ```
  Run the next command to set the environment variable GOOGLE_APPLICATION_CREDENTIALS to the path of the key file(downloaded json file). This allows the SDK to use the key file for authentication.
  For windows:
  ```sh
  set GOOGLE_APPLICATION_CREDENTIALS=path\to\your\key\file.json
  ```
 * After cloning the above repository into your desired folder , make sure to add the authentication file in that folder. Create an python virtual environment in your IDE (I've used VSCode) and install the     
  necessary dependencies from the requirements file:
    ```sh
    python -m venv env
    ```
    ```sh
    source env/bin/activate
    ```
    ```sh
    pip install -r requirements.txt
    ```
    Make sure to set your authentication key to your working directory and (Edit gitignore file as well):
    ```sh
    $env:GOOGLE_APPLICATION_CREDENTIALS = "authentication.json"
    ```
  Note: I've used the python interpreter version: 3.10.11
## Project Tasks:
### 1.PDF Processor:
The first task involves creating the DocumentProcessor class, which will be used in our data ingestion pipeline. This class will handle the processing of PDF documents. Initially, we will implement a file uploader widget capable of handling various types of PDF files for ingestion. Then, we will generate unique temporary file names for each uploaded file, which can be used for further processing or storage purposes within the application. Next, we will utilize [PyPDFLoader](https://python.langchain.com/docs/modules/data_connection/document_loaders/pdf/#using-pypdf) from LangChain to process the uploaded files and extract their pages. Subsequently, we will integrate the extracted pages into the designated class variable. Finally, we will conduct testing using Streamlit run to verify the functionality of the ingestion and processing pipeline for PDF documents. You can see the output below:


### 2.Embeddings:
In this task, we will create word embeddings by utilizing the Vertex AI embeddings through [LangChain](https://python.langchain.com/docs/integrations/text_embedding/google_generative_ai/), passing our project name and model name ("textembedding-gecko@003"). I have tested the word embeddings for the text "Hello World!". You can see the vectors below:

### 3.ChromaDB:
In this task, after processing the PDF files using the DocumentProcessor instance, we will split the processed document into text chunks, which will be more suitable for embeddings. For splitting, I used the [CharacterTextSplitter](https://python.langchain.com/docs/modules/data_connection/document_transformers/character_text_splitter/) function from LangChain. Next, we will store those chunks in the Chroma database using the [Chroma.from_documents](https://python.langchain.com/docs/integrations/vectorstores/chroma/#use-openai-embeddings) function. Eventually, we will create a new method to query the Chroma collection.


### 4.UI for data ingestion:
After successfully instantiating DocumentProcessor, EmbeddingClient, and ChromaCollectionCreator from previous tasks, now it's time to create a user interface by leveraging Streamlit to prompt users to input the quiz's topic and select the desired number of questions via a slider component as shown in the below output. Additionally, we will be utilizing the query Chroma collection method from the previous task so that users can input a query pertinent to the quiz topic. By utilizing the generated Chroma collection, it will extract relevant information corresponding to the query for quiz question generation.


### 5. Creating Quiz Generator class:
We will create an QuizGenerator class , then initialize LLM ([I have used 'Gemini-pro'](https://python.langchain.com/docs/integrations/llms/google_vertex_ai_palm/)) with respective [template](https://python.langchain.com/docs/modules/model_io/prompts/few_shot_examples/) prompt and structure for the quiz, and vectorstore database from the previous task, then we will be using [as_retriever]((https://python.langchain.com/docs/integrations/vectorstores/chroma/#retriever-options)) function to retrieve relevant context for the quiz topic from the vectorstore. Now, to format the retrieved context and the quiz topic into a structured prompt(template) I have used the libraries including [RunnablePassthrough and RunnableParallel from LangChain](https://python.langchain.com/docs/expression_language/primitives/passthrough/) (refer the documentation for better understanding) passed them into the chain and by invoking it with the topic as a input, it generated the expected response and you can see the output below:

  
### 6. Quiz Algorithm:
In this task, we will create the QuizGenerator class, define a generate quiz method, and validate quiz method which allow for the generation of a unique quiz with the desired number of questions while ensuring the uniqueness of each question. After generating the relevant string (response) from the previous task (by invoking the chain with the topic), make sure to convert it into Python dictionary format. I have used the [json.loads()](https://docs.python.org/3/library/json.html) function as the data is in JSON format. See the output below:


### 7. UI for Quiz:
Now, we will work on the QuizManager class, focusing on the indexes of the respective questions, and implement the functionality to display quiz questions and choices on the UI by utilizing Streamlit.

### 8. Screen State Handling:

In the final task, we will generate the quiz by utilizing the necessary classes from the previous tasks and passing the respective arguments. See the final task's(Generative Quiz) demo below:


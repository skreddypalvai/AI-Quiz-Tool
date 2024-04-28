# Quizzify: AI Quiz Generative Tool
## About:
Quizzify is an AI Quiz tool which is powered by large language model (Google – GEMINI). It focuses on providing individuals especially students with accessible and effective means to reinforce their understanding of various topics. Utilizing cutting edge AI methodologies, the tool dynamically generates quizzes based on user provided documents, facilitated by LangChain for document processing and connecting to LLM. It further enhances the learning experience through the integration of Vertex AI for embeddings and the GEMINI large language model. ChromaDB serves as the repository for storing these embeddings, ensuring efficient data management. Moreover, Quizzify leverages Streamlit for its user interfaces, providing an intuitive and interactive platform for users to engage with generated quizzes.
## Initial Setup:
* In order to use Vertex AI services, you have to sign in to Google cloud and redirect to console and initiate an new project, then enable the recommended API in Vertex AI service and you can explore the pretrained models. Next step is to select the IAM & Admin, select the service account and then create an service account where you can access the authentication keys for your google cloud services. While creating the service accounts make sure to select the basic role with owner as a subrole in the service account filter. Then select the service account you created and redirect to key section and select add key with json format. Next you need to install the gcloud CLI(Command Line Interface), after downloading run necessary commands in the GCloud SDK Shell that includes initializing the SDK: 
  ```sh
  gcloud init
  ```
  Run the next command to set the environment variable GOOGLE_APPLICATION_CREDENTIALS to the path of the key file(downloaded json file). This allows the SDK to use the key file for authentication.
  For windows:
  ```sh
  set GOOGLE_APPLICATION_CREDENTIALS=path\to\your\key\file.json
  ```
  Now you are eligible to use the Vertex AI services.
* After cloning the above repository into your desired folder , make sure to add the authentication file in that folder. Create an python virtual environment in your IDE (I've used VSCode) and install the necessary dependencies from the requirements file:
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
We can see the first task is to create the document processor class which will be using for our data ingestion pipeline. This will process the pdf documents and 

  

import os
import streamlit as st 
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import CSVLoader, PyPDFLoader, TextLoader, UnstructuredExcelLoader, Docx2txtLoader
from langchain.document_loaders.base import BaseLoader
from langchain.vectorstores import FAISS
from langchain.vectorstores.chroma import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.chat_models import ChatAnyscale
from dotenv import load_dotenv
load_dotenv()

ANYSCALE_API_KEY=os.getenv('ANYSCALE_API_KEY')
ANYSCALE_API_KEY=ANYSCALE_API_KEY
os.environ["ANYSCALE_API_BASE"]='https://api.endpoints.anyscale.com/v1'
os.environ['ANYSCALE_API_KEY']=ANYSCALE_API_KEY
ANYSCALE_MODEL_NAME='meta-llama/Meta-Llama-3-70B-Instruct'

DOCUMENT_MAP = {
    ".txt": TextLoader,
    ".md": TextLoader,
    ".py": TextLoader,
    ".pdf": PyPDFLoader,
    ".csv": CSVLoader,
    ".xls": UnstructuredExcelLoader,
    ".xlsx": UnstructuredExcelLoader,
    ".docx": Docx2txtLoader,
    ".doc": Docx2txtLoader,
}

def get_file_type(file_path: str):
    return os.path.splitext(file_path)[1]

def load_data(file_path: str) -> BaseLoader:
    """Loads a file and returns a Document object.
    Args:
        file_path: Path to the text file.
    Returns:
        A Document loader object.
    """
    file_type = get_file_type(file_path)
    # print(f"loaded file type - {file_type}")
    loader_class = DOCUMENT_MAP.get(file_type)
    if loader_class is None:
        raise ValueError("File type is not supported!")
    if file_type == ".txt":
        return loader_class(file_path, encoding = 'UTF-8')
    return loader_class(file_path)

@st.cache_resource
def define_question_prompt():
    prompt_template = """
    Have a conversation with a human where you are a advisor which parse the provided document and answer the questions based on it.
    Answer the human questions based on the provided document in pricise manner.'
    If answer is not is document then return don't have answer
    If human is greeting you, greet back politely.
    Do not use any previous knowledge.
    
    {context}

    question: {question}
    anwser:"""
    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )
    chain_type_kwargs = {"prompt": PROMPT,'verbose': False}
    return chain_type_kwargs

@st.cache_resource
def load_document_and_prepare_embeddings(file_path):
    
    EMBEDDING_PATH = f"{os.getcwd()}/embeddings/vectorstore"
    print("Data File 2 - ", file_path)
    loader = PyPDFLoader(file_path)
    print("Data File 3 - ", file_path)
    document = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=300)
    texts = text_splitter.split_documents(document)

    vectorstore  = Chroma.from_documents(texts, OpenAIEmbeddings(deployment='text-embedding-ada-002'), persist_directory=EMBEDDING_PATH)
    print("Embeddings created and saved on system.")
    return vectorstore

@st.cache_resource
def setup_insurance_agent_llama(file_path):
    """Create RetrivalQA langchain agent for Insurance AI Agent
    
    """
    print("Data File - ", file_path)
    vectorstore = load_document_and_prepare_embeddings(file_path)
    base_retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k":3})
    #QA_CHAIN_PROMPT = define_question_prompt()
    chain_type_kwargs = define_question_prompt()
    insurance_qa = RetrievalQA.from_chain_type(llm=ChatAnyscale(model_name=ANYSCALE_MODEL_NAME,temperature=0.0), chain_type="stuff", retriever=base_retriever, 
                                 return_source_documents=False, chain_type_kwargs=chain_type_kwargs)
    return insurance_qa
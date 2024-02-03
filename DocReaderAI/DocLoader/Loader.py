from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

from dotenv import load_dotenv

load_dotenv()
embeddings = OpenAIEmbeddings()


# To load some docs
class Loader:

    # Load PDF
    @staticmethod
    def loadPdfFile(url):
        loader = PyPDFLoader(url)
        return loader.load()

    # Load web base doc {a web page, for instance}
    @staticmethod
    def loadWebBaseDoc(url):
        loader = WebBaseLoader(url)
        return loader.load()

    # Parser
    @staticmethod
    def transform2Vectors(rawTextDoc):

        textSplitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )
        docs = textSplitter.split_documents(rawTextDoc)

        # Covert to the vector and save it
        savedVectoralData = FAISS.from_documents(docs, embeddings)
        return savedVectoralData

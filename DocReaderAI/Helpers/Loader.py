from icecream import ic
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

    loadedFiles = []

    # Retuns length of the loaded files
    @staticmethod
    def getLenghtOfLoadedFiles():
        return len(Loader.loadedFiles)

    # just for debuggin
    # print(str(Loader))
    def __str__(self):
        ic(Loader.loadedFiles)
        return ""

    @staticmethod
    def combineAllLoadedFiles():
        files = Loader.loadedFiles
        pages = []
        for file in files:
            for page in file:
                pages.append(page)

        return pages

    # Load PDF
    @staticmethod
    def loadPdfFile(url):
        # Summarize the file when loaded. An save it
        # put it to the database
        loader = PyPDFLoader(url)

        loadedFile = loader.load()
        Loader.loadedFiles.append(loadedFile)
        return loadedFile

    # Load web base doc {a web page, for instance}
    @staticmethod
    def loadWebBaseDoc(url):
        loader = WebBaseLoader(url)
        loadedFile = loader.load()
        Loader.loadedFiles.append(loadedFile)
        return loadedFile

    @staticmethod
    def splitter(**kwargs):
        return RecursiveCharacterTextSplitter(**kwargs)

    @staticmethod
    def splitteText(text):

        textSplitter = Loader.splitter(chunk_size=400, chunk_overlap=200)
        return textSplitter.split_text(text)

    @staticmethod
    def splitteDocuments(text):

        textSplitter = Loader.splitter(chunk_size=400, chunk_overlap=200)
        return textSplitter.split_documents(text)

    # Parser
    @staticmethod
    def transform2Vectors(rawTextDoc):

        docs = Loader.splitteDocuments(rawTextDoc)

        # Covert to the vector and save it
        savedVectoralData = FAISS.from_documents(docs, embeddings)
        return savedVectoralData

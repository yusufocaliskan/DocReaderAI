from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

from dotenv import load_dotenv

load_dotenv()
openAIEmbeddings = OpenAIEmbeddings()


class Textor:
    @staticmethod
    def splitter(**kwargs):
        return RecursiveCharacterTextSplitter(**kwargs)

    @staticmethod
    def splitteText(text):

        textSplitter = Textor.splitter(chunk_size=400, chunk_overlap=200)
        return textSplitter.split_text(text)

    @staticmethod
    def splitteDocuments(text):

        textSplitter = Textor.splitter(chunk_size=400, chunk_overlap=200)
        return textSplitter.split_documents(text)

    # Parser
    @staticmethod
    def transform2Vectors(rawTextDoc):

        docs = Textor.splitteDocuments(rawTextDoc)

        # Covert to the vector and save it
        savedVectoralData = FAISS.from_documents(docs, openAIEmbeddings)
        return savedVectoralData

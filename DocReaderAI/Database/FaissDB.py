from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

from DocReaderAI.Helpers.Textor import Textor

load_dotenv()


class FaissDB:

    # The embeddings Generator
    embeddings: OpenAIEmbeddings

    # Index name of the vector search
    faissLocalIndexName = "faissDataIndex"

    # index nama of the local db
    vectorDBInstance = None

    # Dimantion
    dimantion = 1536  # OpenAI embeddings amount

    def __init__(self, docs) -> None:

        self.embeddings = OpenAIEmbeddings()

        # Create vector doc
        self.vectorDBInstance = self.createDBFromDocument(docs=docs)

        # And save it
        # self.getTheSavedLocalDB()

    def createDBFromDocument(self, docs):
        """Generates faiss vector vecktorstore"""

        splittedDocs = Textor.splitteDocuments(docs)
        db = FAISS.from_documents(splittedDocs, self.embeddings)
        return db

    # Save it to the load
    # We will then use it
    def saveTheDBInLocal(self):
        FAISS.save_local(self.faissLocalIndexName)

    # Loads the data base saved in local
    def getTheSavedLocalDB(self):
        FAISS.load_local(self.faissLocalIndexName, self.embeddings)

    def embbedingTextQuery(self, text):
        """Basically Embedding a text in order to use with similarity_search_by_vector() methodd"""
        return self.embeddings.embed_query(text)
